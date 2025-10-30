from app.forms import *
from app.services import *
from app.models import *
from app.repositories import *


class Controller:

    def home():
        return "pass"

    def create_shipment():
        return CreateShipmentForm()

    def show_shipment():
        return "pass"

    def edit_shipment():
        return EditTypeForm()

    def type_floor(registration_number):
        return {
            "form": EditTypeFloorForm(),
            "shipment": ShipmentRepository.get_shipment(registration_number),
        }

    def type_pallet(registration_number):
        return {
            "form": BatchEntryForm(),
            "shipment": ShipmentRepository.get_shipment(registration_number),
        }

    def type_trailer(registration_number):

        items = Trailer.query.all()
        form = EditTypeTrailerForm()
        form.choice.choices = [(item.id, item.id) for item in items]

        ShipmentRepository.get_shipment(registration_number)
        return {
            "form": form,
            "shipment": ShipmentRepository.get_shipment(registration_number),
        }

    def settings():
        return {
            "settings-form": EditSettingForm(),
            "batch-form": BatchEntryForm(),
        }
