from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from config import Config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    from app import models  # noqa: F401
    from app.controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp)

    @app.route("/")
    def inicio():
        return redirect(url_for("auth.panel"))

    @app.route("/db-test")
    def db_test():
        try:
            db.session.execute(text("SELECT 1"))
            return "Conexión a la base de datos OK"
        except Exception as e:
            return f"Error de conexión: {e}", 500

    @app.errorhandler(403)
    def acceso_denegado(e):
        return "Acceso denegado: no tiene permisos para esta sección", 403

    return app