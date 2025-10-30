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

    @staticmethod
    def home():
        return "pass"

    @staticmethod
    def create_shipment():
        return CreateShipmentForm()

    @staticmethod
    def show_shipment():
        return "pass"

    @staticmethod
    def edit_shipment():
        return EditTypeForm()

    @staticmethod
    def type_floor(registration_number):
        return {
            "form": EditTypeFloorForm(),
            "shipment": ShipmentRepository.get_shipment(registration_number),
        }

    @staticmethod
    def type_pallet(registration_number):
        return {
            "form": BatchEntryForm(),
            "shipment": ShipmentRepository.get_shipment(registration_number),
        }

    @staticmethod
    def type_trailer(registration_number):
        items = Trailer.query.all()
        form = EditTypeTrailerForm()
        form.choice.choices = [(item.id, item.id) for item in items]

        return {
            "form": form,
            "shipment": ShipmentRepository.get_shipment(registration_number),
        }
