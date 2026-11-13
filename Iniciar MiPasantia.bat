@echo off
cd /d "%~dp0MiPasantia"

if not exist ".venv\Scripts\python.exe" (
    python -m venv .venv
    if errorlevel 1 goto error
)

".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto error

echo Abriendo MiPasantia en http://127.0.0.1:5000
echo Para detener la aplicacion, cierra esta ventana o presiona Ctrl+C.
".venv\Scripts\python.exe" -c "import webbrowser; from werkzeug.serving import make_server; from app import app; server = make_server('127.0.0.1', 5000, app); webbrowser.open('http://127.0.0.1:5000'); server.serve_forever()"
if errorlevel 1 goto error
exit /b 0

:error
echo.
echo No se pudo iniciar MiPasantia. Comprueba que Python este instalado, que haya conexion a Internet y que el puerto 5000 este libre.
pause
exit /b 1
