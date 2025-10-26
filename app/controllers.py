from .forms import Forms
from .services import Services
from .models import Pallet, Trailer
from .logging import logger


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
            "form": Forms.BatchEntryForm(),
            "shipment": Services.DatabaseMethods.get_shipment(registration_number),
        }

    def type_trailer(registration_number):

        items = Trailer.query.all()
        form = Forms.EditTypeTrailerForm()
        form.choice.choices = [(item.id, item.id) for item in items]

        Services.DatabaseMethods.get_shipment(registration_number)
        return {
            "form": form,
            "shipment": Services.DatabaseMethods.get_shipment(registration_number),
        }

    def settings():
        return {
            "settings-form": Forms.EditSettingForm(),
            "batch-form": Forms.BatchEntryForm(),
        }

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
    # Needs to verify that trailer is there
    @staticmethod
    def handle_move_to_trailer(shipment, trailer_id):
        if shipment and trailer_id:
            shipment.trailer_id = trailer_id
            Services.DatabaseMethods.update(shipment)

    # Needs validation to verify pallet is empty
    # Needs valiadatoin to verify pallet exists
    @staticmethod
    def handle_move_to_pallet(shipment, pallets):
        pass

    @staticmethod
    def add_element(raw_text, type="pallet"):
        elements = Services.HelperMethods.batch_get_elements(raw_text, type)
        db_methods = Services.DatabaseMethods()
        errors = []
        successes = []
        flash = ""
        for element in elements:
            is_valid = db_methods.validate_element(element, type)

            if is_valid:
                successes.append((is_valid, element))

            if not is_valid:
                errors.append((is_valid, element))

        if not errors:
            for element in elements:
                new_element = (
                    Trailer(id=element) if type == "trailer" else Pallet(id=element)
                )
                Services.DatabaseMethods.update(new_element)
            valid_ids = ", ".join([element for _, element in successes])
            flash = f"Success, added {type}: {valid_ids}", "success"
            logger.warning(f"Success, added {type}: {valid_ids}")
        else:
            invalid_ids = ", ".join([element for _, element in errors])
            flash = f"Failed to add {type}: {invalid_ids}", "error"
            logger.warning(f"Failed to add {type}: {invalid_ids}")

        return flash
