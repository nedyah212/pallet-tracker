from app import db


class OversizedGood(db.Model):
    __tablename__ = "oversized_goods"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(25), nullable=False)
    registration_number = db.Column(
        db.String(50), db.ForeignKey("shipments.registration_number"), nullable=True
    )

    shipment = db.relationship("Shipment", back_populates="non_palletized_goods")
