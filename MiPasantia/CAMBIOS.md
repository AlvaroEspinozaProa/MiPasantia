# Cambios realizados en MiPasantia

Este documento registra la reorganización técnica de la aplicación activa. Su objetivo es que el equipo pueda entender qué cambió, por qué se hizo y dónde continuar trabajando.

## Qué se preservó

Las páginas y pruebas originales no se eliminaron. Fueron movidas a la carpeta legacy_estatico para conservarlas como referencia histórica.

La aplicación que se ejecuta ahora usa únicamente:

- app.py
- templates/
- static/
- database.db

## Estructura nueva

| Antes | Ahora | Motivo |
| --- | --- | --- |
| HTML mezclado con Python | templates/ | Flask encuentra y renderiza las páginas desde una sola ubicación. |
| CSS junto a los HTML | static/css/style.css | Los recursos visuales quedan separados de las vistas. |
| Sin JavaScript organizado | static/js/main.js | Las pequeñas mejoras de interfaz tienen un lugar propio. |
| Imágenes sin destino definido | static/uploads/ | Las fotos publicadas tienen una carpeta segura y previsible. |
| Dependencias no declaradas | requirements.txt | Otra persona puede instalar lo necesario para ejecutar el proyecto. |

## Backend y rutas

app.py fue reorganizado para que cada función tenga una responsabilidad clara.

| Ruta | Función |
| --- | --- |
| / | Muestra las experiencias más recientes. |
| /explorar | Busca por palabra y filtra por categoría. |
| /experiencia/id | Muestra un relato completo. |
| /registro | Crea una cuenta. |
| /login | Inicia sesión. |
| /logout | Cierra sesión mediante POST. |
| /publicar | Permite crear una experiencia si hay una sesión iniciada. |

También se agregó una página 404 para direcciones inexistentes.

## Base de datos y seguridad

- La conexión SQLite usa una ruta basada en la ubicación de app.py, por lo que no depende de la carpeta desde donde se ejecute el comando.
- Las consultas reciben parámetros; no se construyen pegando texto ingresado por una persona.
- Las contraseñas se guardan con hash de Werkzeug.
- La clave de sesión se puede definir mediante MIPASANTIA_SECRET_KEY en un archivo .env.
- La tabla de experiencias incorpora el campo opcional imagen. La aplicación conserva compatibilidad con la base existente y lo agrega automáticamente si todavía no está.

## Publicación con imagen

El formulario de publicación permite agregar una foto opcional.

- Formatos: PNG, JPG, JPEG y WebP.
- Límite: 2 MB.
- Destino: static/uploads/.
- El nombre final se genera con un identificador único para evitar colisiones.
- Si la imagen supera el límite, la aplicación informa el problema sin mostrar una página técnica.

Las imágenes subidas no se incluyen en Git porque pueden contener material de prueba o datos personales.

## Interfaz

Las plantillas activas comparten templates/base.html. Esto evita repetir la barra de navegación, los mensajes y el pie de página en cada archivo.

Las páginas incluyen estados importantes:

- Mensajes de registro, inicio de sesión, publicación y errores.
- Resultados vacíos al explorar.
- Redirección a inicio de sesión cuando alguien intenta publicar sin cuenta.
- Respuesta clara si una experiencia no existe.

## Archivos de apoyo

- .env.example: ejemplo para crear una clave de sesión propia.
- .gitignore: evita subir secretos, entorno virtual, cachés de Python e imágenes cargadas.
- README.md: instrucciones rápidas para ejecutar el proyecto.
- requirements.txt: dependencias de Python.

## Validación realizada

Se verificó que:

- app.py compile correctamente.
- El JavaScript de static/js/main.js no tenga errores de sintaxis.
- Inicio, explorar, registro y login respondan correctamente.
- Publicar sin sesión redirija al login.
- Un detalle inexistente devuelva 404.
- El flujo registro → login → publicar complete las redirecciones esperadas.

## Próximos pasos posibles

Estas mejoras no son obligatorias para que el proyecto funcione:

1. Mostrar en el perfil las publicaciones de cada usuario.
2. Editar o eliminar una experiencia propia.
3. Agregar paginación cuando haya muchas publicaciones.
4. Incorporar recuperación de contraseña por correo.
5. Moderar publicaciones antes de hacerlas visibles.
