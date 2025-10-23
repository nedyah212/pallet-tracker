from .forms import Forms
from .services import Services


class Controller:

    def home():
        return "pass"

    def create_shipment():
        return Forms.CreateShipmentForm()

    def show_shipment():
        return "pass"

    def edit_shipment():
        return Forms.EditTypeForm()

    def type_floor(registration_number):
        return {
            "form": Forms.EditTypeFloorForm(),
            "shipment": Services.DatabaseMethods.get_shipment(registration_number),
        }

    def type_pallet(registration_number):
        Services.DatabaseMethods.get_shipment(registration_number)
        return {
            "form": Forms.EditTypePalletForm(),
            "shipment": Services.DatabaseMethods.get_shipment(registration_number),
        }

    def type_trailer(registration_number):
        Services.DatabaseMethods.get_shipment(registration_number)
        return {
            "form": Forms.EditTypeTrailerForm(),
            "shipment": Services.DatabaseMethods.get_shipment(registration_number),
        }

    def settings():
        return "pass"

    def pallet_manager():
        return "pass"

    def trailer_manager():
        return "pass"

    @staticmethod
    def handle_choice(choice):

        if choice == "floor":
            route = "main.type_floor"
        elif choice == "pallet":
            route = "main.type_pallet"
        elif choice == "trailer":
            route = "main.type_trailer"
        else:
            route = None

        return route

    def handle_move_from_trailer(shipment):
        if shipment.trailer_id != None:
            shipment.trailer_id = None
            Services.DatabaseMethods.update_shipment(shipment)

    def handle_move_to_trailer(shipment, trailer_id):
        if shipment and trailer_id:
            shipment.trailer_id = trailer_id
            Services.DatabaseMethods.update_shipment(shipment)
