from app import db


class Pallet(db.Model):
    __tablename__ = "pallets"

    id = db.Column(db.String(4), primary_key=True)
    row = db.Column(db.String(2), nullable=True)
    registration_number = db.Column(
        db.String(50),
        db.ForeignKey("shipments.registration_number", ondelete="SET NULL"),
        nullable=True,
    )

    shipment = db.relationship("Shipment", back_populates="pallets")
