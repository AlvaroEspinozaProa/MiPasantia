import gc
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
original_connect = sqlite3.connect
directorio = tempfile.TemporaryDirectory()
base_prueba = Path(directorio.name) / "test.db"
with patch("sqlite3.connect", side_effect=lambda *args, **kwargs: original_connect(base_prueba)):
    import app as aplicacion
aplicacion.DATABASE_PATH = base_prueba


class ForoTest(unittest.TestCase):
    def setUp(self):
        with aplicacion.conectar_db() as conexion:
            conexion.executescript("DELETE FROM respuestas_foro; DELETE FROM temas_foro; DELETE FROM usuarios;")
        self.client = aplicacion.app.test_client()

    def iniciar_sesion(self):
        self.client.post("/registro", data={"nombre": "Ana", "email": "ana@example.test", "password": "clave123"})
        self.client.post("/login", data={"email": "ana@example.test", "password": "clave123"})
        self.client.get("/foro")
        with self.client.session_transaction() as sesion:
            return sesion["token_foro"]

    def test_paginas_y_acceso(self):
        self.assertEqual(self.client.get("/foro").status_code, 200)
        self.assertEqual(self.client.get("/test-vocacional").status_code, 200)
        self.assertEqual(self.client.post("/foro").status_code, 302)
        self.assertEqual(self.client.get("/foro/999").status_code, 404)

    def test_publicar_y_responder(self):
        token = self.iniciar_sesion()
        self.assertEqual(self.client.post("/foro", data={"titulo": "Tema", "contenido": "Hola"}).status_code, 400)
        self.assertEqual(self.client.post("/foro", data={"token": "á", "titulo": "Tema", "contenido": "Hola"}).status_code, 400)
        self.assertEqual(self.client.post("/foro", data={"token": token, "titulo": " ", "contenido": "Hola"}).status_code, 200)
        respuesta = self.client.post("/foro", data={"token": token, "titulo": "Mi pregunta", "contenido": "<script>mal</script>"})
        self.assertEqual(respuesta.status_code, 302)
        tema = self.client.get(respuesta.location)
        self.assertIn(b"Mi pregunta", tema.data)
        self.assertIn(b"&lt;script&gt;", tema.data)
        self.assertNotIn(b"<script>mal</script>", tema.data)
        self.assertEqual(self.client.post(respuesta.location, data={"token": token, "contenido": "Una respuesta"}).status_code, 302)
        self.assertIn(b"Una respuesta", self.client.get(respuesta.location).data)
        self.assertIn(b"1 respuesta", self.client.get("/foro").data)


if __name__ == "__main__":
    try:
        unittest.main()
    finally:
        gc.collect()
        directorio.cleanup()
