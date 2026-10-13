from app import create_app, db
from app.models import Usuario

app = create_app()

with app.app_context():
    if Usuario.query.filter_by(username="vendedor1").first():
        print("El vendedor ya existe")
    else:
        u = Usuario(nombre="Vendedor 1", username="vendedor1", rol="vendedor")
        u.set_password("vendedor123")
        db.session.add(u)
        db.session.commit()
        print("Vendedor creado")