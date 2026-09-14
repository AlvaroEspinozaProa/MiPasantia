from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = "clave_secreta_mi_pasantia"


# -----------------------------
# CONEXIÓN CON LA BASE DE DATOS
# -----------------------------

def conectar_db():
    conexion = sqlite3.connect("database.db")
    conexion.row_factory = sqlite3.Row
    return conexion


# -----------------------------
# CREAR TABLAS
# -----------------------------

def crear_tablas():

    conexion = conectar_db()
    cursor = conexion.cursor()

    # Tabla de usuarios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Tabla de categorías
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE
        )
    """)

    # Tabla de experiencias
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS experiencias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            empresa TEXT NOT NULL,
            contenido TEXT NOT NULL,
            fecha TEXT NOT NULL,
            usuario_id INTEGER,
            categoria_id INTEGER,

            FOREIGN KEY (usuario_id)
            REFERENCES usuarios(id),

            FOREIGN KEY (categoria_id)
            REFERENCES categorias(id)
        )
    """)

    # Categorías predeterminadas
    categorias = [
        "Administración",
        "Comunicación y Marketing",
        "Diseño",
        "Informática y Tecnología",
        "Salud",
        "Educación",
        "Comercio",
        "Gastronomía",
        "Industria",
        "Otra"
    ]

    for categoria in categorias:

        cursor.execute("""
            INSERT OR IGNORE INTO categorias (nombre)
            VALUES (?)
        """, (categoria,))

    conexion.commit()
    conexion.close()
    
@app.route("/")
def index():

    conexion = conectar_db()

    experiencias = conexion.execute("""
        SELECT
            experiencias.*,
            usuarios.nombre AS autor,
            categorias.nombre AS categoria

        FROM experiencias

        JOIN usuarios
        ON experiencias.usuario_id = usuarios.id

        LEFT JOIN categorias
        ON experiencias.categoria_id = categorias.id

        ORDER BY experiencias.id DESC
    """).fetchall()

    conexion.close()

    return render_template(
        "index.html",
        experiencias=experiencias
    )

# -----------------------------
# REGISTRO
# -----------------------------

@app.route("/registro", methods=["GET", "POST"])
def registro():

    if request.method == "POST":

        nombre = request.form["nombre"]
        email = request.form["email"]
        password = request.form["password"]

        password_encriptada = generate_password_hash(password)

        conexion = conectar_db()

        try:

            conexion.execute("""
                INSERT INTO usuarios
                (nombre, email, password)
                VALUES (?, ?, ?)
            """, (
                nombre,
                email,
                password_encriptada
            ))

            conexion.commit()
            conexion.close()

            flash("Registro exitoso. Ahora podés iniciar sesión.")

            return redirect(url_for("login"))

        except sqlite3.IntegrityError:

            conexion.close()

            flash("Ese correo electrónico ya está registrado.")

    return render_template("registro.html")


# -----------------------------
# INICIO DE SESIÓN
# -----------------------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conexion = conectar_db()

        usuario = conexion.execute("""
            SELECT *
            FROM usuarios
            WHERE email = ?
        """, (email,)).fetchone()

        conexion.close()

        if usuario and check_password_hash(
            usuario["password"],
            password
        ):

            session["usuario_id"] = usuario["id"]
            session["nombre"] = usuario["nombre"]

            return redirect(url_for("index"))

        else:

            flash("El correo o la contraseña son incorrectos.")

    return render_template("login.html")


# -----------------------------
# CERRAR SESIÓN
# -----------------------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("index"))


# -----------------------------
# PUBLICAR EXPERIENCIA
# -----------------------------

@app.route("/publicar", methods=["GET", "POST"])
@app.route("/publicar", methods=["GET", "POST"])
def publicar():

    if "usuario_id" not in session:

        flash("Tenés que iniciar sesión para publicar.")

        return redirect(url_for("login"))

    conexion = conectar_db()

    categorias = conexion.execute("""
        SELECT *
        FROM categorias
        ORDER BY nombre
    """).fetchall()

    conexion.close()

    if request.method == "POST":

        titulo = request.form["titulo"]

        empresa = request.form["empresa"]

        contenido = request.form["contenido"]

        fecha = request.form["fecha"]

        categoria_id = request.form["categoria_id"]

        conexion = conectar_db()

        conexion.execute("""
            INSERT INTO experiencias
            (
                titulo,
                empresa,
                contenido,
                fecha,
                usuario_id,
                categoria_id
            )

            VALUES (?, ?, ?, ?, ?, ?)
        """, (

            titulo,

            empresa,

            contenido,

            fecha,

            session["usuario_id"],

            categoria_id

        ))

        conexion.commit()

        conexion.close()

        flash("Tu experiencia fue publicada.")

        return redirect(url_for("index"))

    return render_template(
        "publicar.html",
        categorias=categorias
    )
def experiencia(id):

    conexion = conectar_db()

    experiencia = conexion.execute("""
        SELECT experiencias.*, usuarios.nombre
        FROM experiencias
        JOIN usuarios
        ON experiencias.usuario_id = usuarios.id
        WHERE experiencias.id = ?
    """, (id,)).fetchone()

    conexion.close()

    return render_template(
        "experiencia.html",
        experiencia=experiencia
    )


# -----------------------------
# EJECUTAR APLICACIÓN
# -----------------------------

if __name__ == "__main__":

    crear_tablas()

    app.run(debug=True)
    from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "clave-secreta"

db = SQLAlchemy(app)


# =========================
# MODELO DE PUBLICACIONES
# =========================

class ForoPost(db.Model):
    __tablename__ = "foro_posts"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    respuestas = db.relationship(
        "ForoRespuesta",
        backref="post",
        lazy=True,
        cascade="all, delete-orphan"
    )


# =========================
# MODELO DE RESPUESTAS
# =========================

class ForoRespuesta(db.Model):
    __tablename__ = "foro_respuestas"

    id = db.Column(db.Integer, primary_key=True)
    contenido = db.Column(db.Text, nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    post_id = db.Column(
        db.Integer,
        db.ForeignKey("foro_posts.id"),
        nullable=False
    )

