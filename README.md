  # Minimarket Primavera

  Sistema de gestión de inventario y ventas para Minimarket Primavera.
  Curso: Lenguajes de Programación (UTP). Python + Flask, PostgreSQL en Neon, patrón MVC.

  ## Requisitos
  - Python 3.13
  - Una base PostgreSQL (local o en la nube)

  ## Instalación
```
  python -m venv venv
  venv\Scripts\activate
  pip install -r requirements.txt
```

  ## Configuración
  1. Copia `.env.example` como `.env`.
  2. Escribe tu `DATABASE_URL` y una `SECRET_KEY` propia.
  3. Ejecuta el script DDL en tu base de datos para crear las tablas.

  ## Ejecución
```
  python run.py
```
  Abre http://127.0.0.1:5000/login

  ## Integrantes
  1. Fabio Cruz
  2. Josue Biminchumo
  3. Enrique Dextre
  4. Jose Carlos Olivares
  5. Mathias Herrera