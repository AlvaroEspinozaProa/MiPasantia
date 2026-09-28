"""Aplicación principal de MiPasantia."""

import os
import sqlite3
from pathlib import Path
from uuid import uuid4

from flask import Flask, abort, flash, redirect, render_template, request, session, url_for
from dotenv import load_dotenv
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename


# Rutas que no dependen de dónde se ejecute el comando.
BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "database.db"
UPLOAD_DIR = BASE_DIR / "static" / "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

# Lee variables locales sin subir secretos al repositorio.
load_dotenv(BASE_DIR / ".env")

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("MIPASANTIA_SECRET_KEY", "cambiar-esta-clave-en-produccion")
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024  # Máximo: 2 MB por imagen.


def conectar_db():
    """Abre una conexión SQLite que permite leer columnas por nombre."""
    conexion = sqlite3.connect(DATABASE_PATH)
    conexion.row_factory = sqlite3.Row
    return conexion


def crear_tablas():
    """Crea las tablas y categorías necesarias la primera vez."""
    categorias = (
        "Administración",
        "Comunicación y Marketing",
        "Diseño",
        "Informática y Tecnología",
        "Salud",
        "Educación",
        "Comercio",
        "Gastronomía",
        "Industria",
        "Otra",
    )

    with conectar_db() as conexion:
        conexion.executescript(
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS categorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE
            );

            CREATE TABLE IF NOT EXISTS experiencias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                empresa TEXT NOT NULL,
                contenido TEXT NOT NULL,
                fecha TEXT NOT NULL,
                imagen TEXT,
                usuario_id INTEGER NOT NULL,
                categoria_id INTEGER,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
                FOREIGN KEY (categoria_id) REFERENCES categorias(id)
            );
            """
        )

        # Mantiene compatibilidad con una base creada antes de agregar imágenes.
        columnas = {columna["name"] for columna in conexion.execute("PRAGMA table_info(experiencias)")}
        if "imagen" not in columnas:
            conexion.execute("ALTER TABLE experiencias ADD COLUMN imagen TEXT")

        conexion.executemany(
            "INSERT OR IGNORE INTO categorias (nombre) VALUES (?)",
            ((categoria,) for categoria in categorias),
        )


def obtener_categorias():
    """Devuelve categorías ordenadas para formularios y filtros."""
    with conectar_db() as conexion:
        return conexion.execute("SELECT * FROM categorias ORDER BY nombre").fetchall()


def obtener_experiencias(busqueda="", categoria_id=""):
    """Busca experiencias sin construir SQL con texto del usuario."""
    consulta = """
        SELECT experiencias.*, usuarios.nombre AS autor, categorias.nombre AS categoria
        FROM experiencias
        JOIN usuarios ON experiencias.usuario_id = usuarios.id
        LEFT JOIN categorias ON experiencias.categoria_id = categorias.id
        WHERE 1 = 1
    """
    parametros = []

    if busqueda:
        consulta += " AND (experiencias.titulo LIKE ? OR experiencias.empresa LIKE ? OR experiencias.contenido LIKE ?)"
        termino = f"%{busqueda}%"
        parametros.extend((termino, termino, termino))

    if categoria_id.isdigit():
        consulta += " AND experiencias.categoria_id = ?"
        parametros.append(categoria_id)

    consulta += " ORDER BY experiencias.id DESC"
    with conectar_db() as conexion:
        return conexion.execute(consulta, parametros).fetchall()


def extension_permitida(nombre_archivo):
    """Comprueba que la extensión pertenezca a las imágenes admitidas."""
    return "." in nombre_archivo and nombre_archivo.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def guardar_imagen(archivo):
    """Guarda una imagen opcional y devuelve su ruta pública."""
    if not archivo or not archivo.filename:
        return None

    if not extension_permitida(archivo.filename):
        raise ValueError("La imagen debe ser PNG, JPG, JPEG o WebP.")

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    nombre = secure_filename(archivo.filename)
    destino = UPLOAD_DIR / f"{uuid4().hex}_{nombre}"
    archivo.save(destino)
    return f"uploads/{destino.name}"


def usuario_logueado():
    """Evita repetir la comprobación de sesión en las rutas privadas."""
    return session.get("usuario_id") is not None


@app.route("/")
def index():
    """Muestra las experiencias más recientes."""
    return render_template("index.html", experiencias=obtener_experiencias()[:6])


@app.route("/explorar")
def explorar():
    """Permite buscar por texto y filtrar por categoría."""
    busqueda = request.args.get("q", "").strip()
    categoria_id = request.args.get("categoria", "")
    return render_template(
        "explorar.html",
        experiencias=obtener_experiencias(busqueda, categoria_id),
        categorias=obtener_categorias(),
        busqueda=busqueda,
        categoria_id=categoria_id,
    )


@app.route("/experiencia/<int:experiencia_id>")
def experiencia(experiencia_id):
    """Muestra el relato completo de una publicación."""
    with conectar_db() as conexion:
        resultado = conexion.execute(
            """
            SELECT experiencias.*, usuarios.nombre AS autor, categorias.nombre AS categoria
            FROM experiencias
            JOIN usuarios ON experiencias.usuario_id = usuarios.id
            LEFT JOIN categorias ON experiencias.categoria_id = categorias.id
            WHERE experiencias.id = ?
            """,
            (experiencia_id,),
        ).fetchone()

    if resultado is None:
        abort(404)
    return render_template("experiencia.html", experiencia=resultado)


@app.route("/registro", methods=["GET", "POST"])
def registro():
    """Registra una cuenta y guarda solamente el hash de su contraseña."""
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not nombre or not email or len(password) < 6:
            flash("Completá tu nombre, correo y una contraseña de al menos 6 caracteres.", "error")
        else:
            try:
                with conectar_db() as conexion:
                    conexion.execute(
                        "INSERT INTO usuarios (nombre, email, password) VALUES (?, ?, ?)",
                        (nombre, email, generate_password_hash(password)),
                    )
                flash("Registro exitoso. Ahora podés iniciar sesión.", "ok")
                return redirect(url_for("login"))
            except sqlite3.IntegrityError:
                flash("Ese correo electrónico ya está registrado.", "error")

    return render_template("registro.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Inicia sesión después de verificar el hash de contraseña."""
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        with conectar_db() as conexion:
            usuario = conexion.execute("SELECT * FROM usuarios WHERE email = ?", (email,)).fetchone()

        if usuario and check_password_hash(usuario["password"], password):
            session.clear()
            session["usuario_id"] = usuario["id"]
            session["nombre"] = usuario["nombre"]
            flash(f"Bienvenido/a, {usuario['nombre']}.", "ok")
            return redirect(url_for("index"))

        flash("El correo o la contraseña son incorrectos.", "error")

    return render_template("login.html")


@app.post("/logout")
def logout():
    """Cierra la sesión actual."""
    session.clear()
    flash("Cerraste sesión.", "ok")
    return redirect(url_for("index"))


@app.route("/publicar", methods=["GET", "POST"])
def publicar():
    """Crea una experiencia asociada al usuario que inició sesión."""
    if not usuario_logueado():
        flash("Tenés que iniciar sesión para publicar.", "error")
        return redirect(url_for("login"))

    categorias = obtener_categorias()
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        empresa = request.form.get("empresa", "").strip()
        contenido = request.form.get("contenido", "").strip()
        fecha = request.form.get("fecha", "")
        categoria_id = request.form.get("categoria_id", "")

        if not all((titulo, empresa, contenido, fecha, categoria_id.isdigit())):
            flash("Completá todos los campos obligatorios.", "error")
        else:
            try:
                imagen = guardar_imagen(request.files.get("imagen"))
                with conectar_db() as conexion:
                    conexion.execute(
                        """
                        INSERT INTO experiencias (titulo, empresa, contenido, fecha, imagen, usuario_id, categoria_id)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        """,
                        (titulo, empresa, contenido, fecha, imagen, session["usuario_id"], categoria_id),
                    )
                flash("Tu experiencia fue publicada.", "ok")
                return redirect(url_for("index"))
            except ValueError as error:
                flash(str(error), "error")

    return render_template("publicar.html", categorias=categorias)


@app.errorhandler(404)
def pagina_no_encontrada(error):
    """Muestra una salida clara cuando una dirección no existe."""
    return render_template("404.html"), 404


@app.errorhandler(RequestEntityTooLarge)
def imagen_demasiado_grande(error):
    """Informa el límite de carga sin mostrar una página técnica."""
    flash("La imagen supera el límite de 2 MB.", "error")
    return redirect(url_for("publicar"))


crear_tablas()

if __name__ == "__main__":
    app.run(debug=True)
