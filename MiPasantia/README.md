# MiPasantia

Aplicación Flask para compartir experiencias de pasantías estudiantiles.

## Ejecutar

1. Crear y activar un entorno virtual.
2. Instalar las dependencias con pip install -r requirements.txt.
3. Copiar .env.example como .env y definir una clave secreta propia.
4. Ejecutar python app.py.
5. Abrir http://127.0.0.1:5000.

## Organización

- app.py: rutas, consultas y validaciones.
- templates/: HTML renderizado por Flask y Jinja.
- static/: estilos, JavaScript e imágenes subidas.
- Guía de Trabajo.md y Guia_de_trabajo_MiPasantia.md: material de apoyo para el equipo.

Las contraseñas se guardan con hash. Las imágenes publicadas se almacenan en static/uploads/ y no se suben al repositorio.

La base SQLite se crea automáticamente al iniciar la aplicación y permanece en esta carpeta. Es una versión de desarrollo: antes de publicarla en Internet necesita una revisión de seguridad y una configuración de producción.

Para conocer la reorganización y las pruebas realizadas, consultar CAMBIOS.md.
