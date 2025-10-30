# app/controllers/shipments_controller.py
from app.forms import (
    CreateShipmentForm,
    EditTypeForm,
    EditTypeFloorForm,
    EditTypeTrailerForm,
    BatchEntryForm,
)
from app.models import Trailer
from app.repositories import ShipmentRepository


class ShipmentsController:
    def __init__(self, shipment_repo=None):
        self.shipment_repo = shipment_repo or ShipmentRepository()

    def home(self):
        return "pass"

    def create_shipment(self):
        return CreateShipmentForm()

    def show_shipment(self):
        return "pass"

    def edit_shipment(self):
        return EditTypeForm()

    def type_floor(self, registration_number):
        return {
            "form": EditTypeFloorForm(),
            "shipment": self.shipment_repo.get_shipment(registration_number),
        }

    def type_pallet(self, registration_number):
        return {
            "form": BatchEntryForm(),
            "shipment": self.shipment_repo.get_shipment(registration_number),
        }

    def type_trailer(self, registration_number):
        items = Trailer.query.all()
        form = EditTypeTrailerForm()
        form.choice.choices = [(item.id, item.id) for item in items]

        return {
            "form": form,
            "shipment": self.shipment_repo.get_shipment(registration_number),
        }
