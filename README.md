# FutureHub / Mi Pasantía

Plataforma para que estudiantes compartan experiencias de pasantías, conozcan empresas y accedan a recursos de orientación.

## Estructura

- `MiPasantia/`: aplicación principal (Flask, plantillas HTML, estilos y base de datos SQLite).
- `maqueta_mipasantia/`: referencia visual y funcional independiente; guarda sus datos ficticios en el navegador.
- `prototipos/organizador-escolar/`: prototipo independiente de horarios, materias y test.
- `archivo/`: copias históricas conservadas solo como respaldo. No forman parte de la aplicación activa.
- `Guía de Trabajo.md`: consignas y guía de integración de la etapa actual.
- `Guia_de_trabajo_MiPasantia.md`: hoja de ruta profesional para que el equipo continúe el proyecto por etapas.

## Ejecutar la aplicación principal

```powershell
Set-Location MiPasantia
python app.py
```

Luego abrir la dirección que indique Flask, normalmente `http://127.0.0.1:5000`.
