from . import db
from flask import flash
from .logging import logger
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError
from .models import Shipment, Pallet, Trailer, OversizedGood
import re


class Services:

    class HelperMethods:

        def boolean_to_status_string(self, boolean):
            return (
                "At Capacity"
                if boolean
                else "Not at Capacity" if boolean is not None else ""
            )

        @staticmethod
        def remove_delimiters(text):
            return (
                text.replace("-", "").replace(" ", "").replace("/", "")
                if text is not None
                else ""
            )

        @staticmethod
        def filter_with_regex(text, type="pallet"):
            if type == "pallet":
                text = re.sub(r"[^0-9,]", "", text)
            elif type == "trailer":
                text = re.sub(r"[^a-zA-Z0-9,]", "", text)
            return text

        @staticmethod
        def batch_get_elements(raw_text, type="pallet"):
            text = Services.HelperMethods.filter_with_regex(raw_text, type)
            text = "".join(text)
            elements = text.split(",")
            elements = [e for e in elements if e != ""]
            return elements

        @staticmethod
        def add_element(raw_text, type="pallet"):
            elements = Services.HelperMethods.batch_get_elements(raw_text, type)
            db_methods = Services.DatabaseMethods()
            errors = []

            for element in elements:
                is_valid = db_methods.validate_element(element, type)

                if not is_valid:
                    errors.append((is_valid, element))

            if not errors:
                for element in elements:
                    new_element = (
                        Trailer(id=element) if type == "trailer" else Pallet(id=element)
                    )
                    Services.DatabaseMethods.update(new_element)
            else:
                invalid_ids = ",".join([element for _, element in errors])
                flash(f"Failed to add {type}(s): {invalid_ids}", "error")
                logger.warning(f"Failed to add {type}(s): {invalid_ids}")

    class ConstructorMethods:
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

        def create_oversized_good(form, desc, loc, reg):
            oversized_good = OversizedGood(
                description=desc, location=loc, registration_number=reg
            )
            return oversized_good

    class DatabaseMethods:
        def create_shipment(shipment):
            try:
                db.session.add(shipment)
                db.session.commit()
                logger.info(f"Success: {shipment} has been added to the database.")
                return True
            except IntegrityError as e:
                logger.error(f"IntegrityError: {e}")
                db.session.rollback()
                return False
            except OperationalError as e:
                logger.error(f"OperationalError: {e}")
                db.session.rollback()
                return False
            except SQLAlchemyError as e:
                logger.error(f"SQLAlchemyError: {e}")
                db.session.rollback()
                return False

        def get_shipment(registration_number):
            try:
                shipment = db.session.get(Shipment, registration_number)
                logger.info(
                    f"Success: Database queried for shipment by registration number."
                )
            except OperationalError as e:
                logger.error(f"OperationalError: {e}")
            except SQLAlchemyError as e:
                logger.error(f"SQLAlchemyError: {e}")
            return shipment

        @staticmethod
        def update(record):
            try:
                db.session.add(record)
                db.session.commit()
            except IntegrityError as e:
                logger.error(f"IntegrityError: {e}")
                db.session.rollback()
                return False
            except OperationalError as e:
                logger.error(f"OperationalError: {e}")
                db.session.rollback()
                return False
            except SQLAlchemyError as e:
                logger.error(f"SQLAlchemyError: {e}")
                db.session.rollback()
                return False

        def get_pallets(registration_number):
            try:
                pallets = Pallet.query.filter_by(
                    registration_number=registration_number
                ).all()
                logger.info(
                    f"Success: Database queried for pallets by registration number."
                )
            except OperationalError as e:
                logger.error(f"OperationalError: {e}")
            except SQLAlchemyError as e:
                logger.error(f"SQLAlchemyError: {e}")
            return pallets

        def validate_element(self, element, type="pallet"):
            try:
                if type == "trailer":
                    record = db.session.get(Trailer, element)
                else:
                    record = db.session.get(Pallet, element)

                record = False if record != None else True
            except OperationalError as e:
                logger.error(f"OperationalError: {e}")
            except SQLAlchemyError as e:
                logger.error(f"SQLAlchemyError: {e}")
            return record
