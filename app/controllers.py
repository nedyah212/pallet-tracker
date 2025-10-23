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
        return "pass"

    def type_pallet():
        return "pass"

    def type_trailer():
        return "pass"

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
