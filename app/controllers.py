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
        return Forms.EditSettingForm()

    def pallet():
        return Forms.BatchEntryForm()

    def trailer():
        return Forms.BatchEntryForm()

    @staticmethod
    def handle_choice(choice, alt=False):
        if choice == "floor":
            route = "main.type_floor"
        elif choice == "pallet":
            route = "main.type_pallet" if alt else "main.pallet"
        elif choice == "trailer":
            route = "main.type_trailer" if alt else "main.trailer"
        else:
            route = None

        return route

    @staticmethod
    def remove_pallet_or_trailer(shipment=None, registration_number=None):

        if shipment and shipment.trailer_id != None:
            shipment.trailer_id = None
            Services.DatabaseMethods.update(shipment)

        if registration_number:
            pallets = Services.DatabaseMethods.get_pallets(registration_number)

            for pallet in pallets:
                pallet.registration_number = None
                Services.DatabaseMethods.update(pallet)

    # Needs validation to check if trailer is full
    @staticmethod
    def handle_move_to_trailer(shipment, trailer_id):
        if shipment and trailer_id:
            shipment.trailer_id = trailer_id
            Services.DatabaseMethods.update(shipment)

    # Needs validation to check if pallet is full
    @staticmethod
    def handle_move_to_pallet(shipment, pallets):
        pass
