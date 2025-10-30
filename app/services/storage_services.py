from ..models import Shipment, Pallet, Trailer, OversizedGood
from app.repositories import *
import re


class StorageServices:

    @staticmethod
    def create_shipment_object(form):
        shipment = Shipment(
            registration_number=form.registration_number.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            tag_colour=form.tag_colour.data,
            tag_code=form.tag_code.data,
            date_received=form.date_received.data,
            date_out=form.date_out.data,
            origin=form.origin.data,
            destination=form.destination.data,
            driver_in=form.driver_in.data,
            driver_out=form.driver_out.data,
            checked_in_by=form.checked_in_by.data,
            checked_out_by=form.checked_out_by.data,
        )
        return shipment

    @staticmethod
    def create_oversized_good(form, desc, loc, reg):
        oversized_good = OversizedGood(
            description=desc, location=loc, registration_number=reg
        )
        return oversized_good

    @staticmethod
    def add_element(elements, elementT):
        records = []
        for element in elements.split(","):
            element = element.strip()

            # Filter by type and regex
            element = re.sub(r"[^a-zA-Z0-9,]", "", element)
            element = element.capitalize()

            # Filter by type and length
            is_valid = False
            if elementT == Pallet:
                if len(element) == 4 and element.isdigit():
                    is_valid = True
            elif elementT == Trailer:
                if len(element) >= 2:
                    is_valid = True

            is_valid = is_valid and ShipmentRepository.mark_invalid_pk(
                element, elementT
            )
            records.append((element, is_valid))

        valid = [el for el, is_valid in records if is_valid]
        invalid = [el for el, is_valid in records if not is_valid]

        if not invalid:
            for element in valid:
                obj = elementT(id=element)
                ShipmentRepository.create_shipment(obj)
            msg = f"Valid {elementT.__name__}: {', '.join(valid)}"
            category = "success"
        else:
            msg = f"Invalid {elementT.__name__}: {', '.join(invalid)}"
            category = "error"

        return msg, category
