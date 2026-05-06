# Aplicación: Nombre y Apellido (FastAPI + SQLite)

Pequeña app que muestra un formulario con dos campos (nombre y apellido) y guarda los envíos en SQLite.

Requisitos:
- Python 3.8+
- Instalar dependencias:
  pip install -r requirements.txt

Ejecutar:
  python main.py

Abrir en el navegador:
  http://127.0.0.1:8000/

Base de datos:
- SQLite en ./app.db (cadena: sqlite:///./app.db, connect_args={'check_same_thread': False})