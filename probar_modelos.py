from decimal import Decimal
from app import create_app, db
from app.models import Usuario, Producto, Venta

app = create_app()

with app.app_context():
    user = Usuario.query.filter_by(username="admin").first()
    if not user:
        user = Usuario(nombre="Administrador", username="admin", rol="administrador")
        user.set_password("admin123")
        db.session.add(user)

    prod = Producto.query.filter_by(codigo="P001").first()
    if not prod:
        prod = Producto(codigo="P001", nombre="Arroz 1kg", categoria="Abarrotes",
                        precio=Decimal("4.50"), stock_actual=10, stock_minimo=3)
        db.session.add(prod)
    db.session.commit()

    print("Stock antes:", prod.stock_actual)

    venta = Venta(metodo_pago="efectivo", monto_recibido=Decimal("20.00"),
                  usuario_id=user.id)
    venta.agregar_detalle(prod, 2)
    venta.confirmar()

    print("Total:", venta.total, "| Vuelto:", venta.vuelto)
    print("Stock después de vender:", prod.stock_actual)
    print("¿Requiere reposición?", prod.requiere_reposicion())

    venta.anular(user, "Prueba de anulación")
    print("Estado:", venta.estado)
    print("Stock tras anular:", prod.stock_actual)