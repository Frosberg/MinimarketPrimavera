from functools import wraps
from flask import (Blueprint, render_template, request, redirect,
                   url_for, session, flash, g, abort)
from app import db
from app.models import Usuario

auth_bp = Blueprint("auth", __name__)


@auth_bp.before_app_request
def cargar_usuario():
    """Carga en g.usuario al usuario de la sesión, si existe y está activo."""
    usuario_id = session.get("usuario_id")
    g.usuario = db.session.get(Usuario, usuario_id) if usuario_id else None
    if g.usuario is not None and not g.usuario.activo:
        session.clear()
        g.usuario = None


def login_requerido(f):
    """Exige que haya un usuario con sesión iniciada."""
    @wraps(f)
    def envoltura(*args, **kwargs):
        if g.usuario is None:
            flash("Debe iniciar sesión para continuar", "error")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return envoltura


def rol_requerido(*roles):
    """Exige sesión iniciada y que el rol del usuario esté entre los permitidos."""
    def decorador(f):
        @wraps(f)
        def envoltura(*args, **kwargs):
            if g.usuario is None:
                flash("Debe iniciar sesión para continuar", "error")
                return redirect(url_for("auth.login"))
            if g.usuario.rol not in roles:
                abort(403)
            return f(*args, **kwargs)
        return envoltura
    return decorador


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        usuario = Usuario.query.filter_by(username=username).first()
        if usuario and usuario.autenticar(password):
            session.clear()
            session["usuario_id"] = usuario.id
            return redirect(url_for("auth.panel"))
        flash("Usuario o contraseña incorrectos", "error")
    return render_template("login.html")


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


@auth_bp.route("/panel")
@login_requerido
def panel():
    return render_template("panel.html")


@auth_bp.route("/admin-prueba")
@rol_requerido("administrador")
def admin_prueba():
    return "Zona exclusiva del administrador: acceso permitido"