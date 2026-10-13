from datetime import datetime
from decimal import Decimal
from app import db
from app.models.detalle_venta import DetalleVenta


class Venta(db.Model):
    __tablename__ = "ventas"

    id = db.Column(db.Integer, primary_key=True)
    fecha_hora = db.Column(db.DateTime, nullable=False, default=datetime.now)
    total = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    metodo_pago = db.Column(db.String(20), nullable=False)
    monto_recibido = db.Column(db.Numeric(10, 2))
    vuelto = db.Column(db.Numeric(10, 2), default=0)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)

    estado = db.Column(db.String(20), nullable=False, default="completada")
    fecha_anulacion = db.Column(db.DateTime)
    motivo_anulacion = db.Column(db.String(255))
    anulada_por = db.Column(db.Integer, db.ForeignKey("usuarios.id"))

    usuario = db.relationship(
        "Usuario", foreign_keys=[usuario_id], backref="ventas"
    )
    detalles = db.relationship(
        "DetalleVenta", backref="venta", cascade="all, delete-orphan"
    )

    def agregar_detalle(self, producto, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")
        if cantidad > producto.stock_actual:
            raise ValueError(f"Stock insuficiente de {producto.nombre}")
        detalle = DetalleVenta(
            producto=producto,
            cantidad=cantidad,
            precio_unitario=producto.precio,
        )
        detalle.calcular_subtotal()
        self.detalles.append(detalle)

    def calcular_total(self):
        self.total = sum((d.subtotal for d in self.detalles), Decimal("0"))
        return self.total

    def calcular_vuelto(self):
        if self.metodo_pago == "efectivo":
            if self.monto_recibido is None or self.monto_recibido < self.total:
                raise ValueError("El monto recibido es menor al total")
            self.vuelto = Decimal(self.monto_recibido) - Decimal(self.total)
        else:
            self.monto_recibido = self.total
            self.vuelto = Decimal("0")
        return self.vuelto

    def confirmar(self):
        """Guarda la venta, sus detalles y el descuento de stock en una sola transacción."""
        try:
            if not self.detalles:
                raise ValueError("La venta no tiene productos")
            self.calcular_total()
            self.calcular_vuelto()
            for d in self.detalles:
                d.producto.descontar_stock(d.cantidad)
            db.session.add(self)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

    def anular(self, usuario, motivo):
        """Anula la venta y devuelve el stock en una sola transacción."""
        try:
            if not usuario.es_admin():
                raise PermissionError("Solo el administrador puede anular ventas")
            if self.estado == "anulada":
                raise ValueError("La venta ya fue anulada")
            if not motivo or not motivo.strip():
                raise ValueError("Debe indicar el motivo de la anulación")
            for d in self.detalles:
                d.producto.reponer_stock(d.cantidad)
            self.estado = "anulada"
            self.fecha_anulacion = datetime.now()
            self.motivo_anulacion = motivo.strip()
            self.anulada_por = usuario.id
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise