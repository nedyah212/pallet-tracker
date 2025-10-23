from .forms import Forms


class Controller:

    def home():
        return "pass"

    def create_shipment():
        return Forms.CreateShipmentForm()

    def show_shipment():
        return "pass"

    def edit_shipment():
        return Forms.EditTypeForm()

    def type_floor():
        return Forms.EditTypeFloorForm()

    def type_pallet():
        return Forms.EditTypePalletForm()

    def type_trailer():
        return Forms.EditTypeTrailerForm()

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
