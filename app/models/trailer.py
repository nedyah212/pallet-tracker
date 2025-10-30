from app import db


class Trailer(db.Model):
    __tablename__ = "trailers"

    id = db.Column(db.String(15), primary_key=True)
    status = db.Column(db.Boolean, default=False)

    shipments = db.relationship(
        "Shipment", back_populates="trailer", cascade="all, delete-orphan"
    )
