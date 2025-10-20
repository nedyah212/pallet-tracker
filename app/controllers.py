from .forms import Forms


class Controller:
    def home():
        return "pass"

    def create_shipment():
        return Forms.CreateShipmentForm()

    def show_shipment():
        return "pass"

    def edit_shipment():
        return "pass"

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
