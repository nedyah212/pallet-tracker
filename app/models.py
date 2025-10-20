from app import db
from sqlalchemy.ext.hybrid import hybrid_property


class Shipment(db.Model):
    __tablename__ = "shipments"

    registration_number = db.Column(db.String(50), primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    tag_colour = db.Column(db.String(15), nullable=True)
    tag_code = db.Column(db.String(30), nullable=True)
    date_received = db.Column(db.DateTime, nullable=True)
    date_out = db.Column(db.DateTime, nullable=True)
    origin = db.Column(db.String(30), nullable=True)
    destination = db.Column(db.String(30), nullable=True)
    driver_in = db.Column(db.String(30), nullable=True)
    driver_out = db.Column(db.String(30), nullable=True)
    checked_in_by = db.Column(db.String(30), nullable=True)
    checked_out_by = db.Column(db.String(30), nullable=True)
    archived = db.Column(db.Boolean, default=False)

    trailer_id = db.Column(db.String(15), db.ForeignKey("trailers.id"), nullable=True)

    trailer = db.relationship("Trailer", back_populates="shipments")
    pallets = db.relationship("Pallet", back_populates="shipment", passive_deletes=True)
    non_palletized_goods = db.relationship(
        "OversizedGood", back_populates="shipment", cascade="all, delete-orphan"
    )

    @hybrid_property
    def shipper_name_reversed(self):
        return self.last_name + ", " + self.first_name


class Pallet(db.Model):
    __tablename__ = "pallets"

    id = db.Column(db.String(5), primary_key=True)
    row = db.Column(db.String(2))
    status = db.Column(db.Boolean)
    registration_number = db.Column(
        db.String(50),
        db.ForeignKey("shipments.registration_number", ondelete="SET NULL"),
        nullable=True,
    )

    shipment = db.relationship("Shipment", back_populates="pallets")


class Trailer(db.Model):
    __tablename__ = "trailers"

    id = db.Column(db.String(15), primary_key=True)
    location = db.Column(db.String(25), nullable=False)
    status = db.Column(db.Boolean)

    shipments = db.relationship(
        "Shipment", back_populates="trailer", cascade="all, delete-orphan"
    )


class OversizedGood(db.Model):
    __tablename__ = "oversized_goods"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(25), nullable=False)
    registration_number = db.Column(
        db.String(50), db.ForeignKey("shipments.registration_number"), nullable=True
    )

    shipment = db.relationship("Shipment", back_populates="non_palletized_goods")
