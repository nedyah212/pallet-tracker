from . import db
from .logging import logger
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError
from .models import Shipment, Pallet, Trailer, OversizedGood
import re


class Services:

    class HelperMethods:

        @staticmethod
        def boolean_to_status_string(boolean):
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
        def filter_with_regex(text, data_type):
            if data_type == Pallet:
                text = re.sub(r"[^0-9,]", "", text)
            elif data_type == Trailer:
                text = re.sub(r"[^a-zA-Z0-9,]", "", text)
                text.capitalize()
            return text

        @staticmethod
        def mark_invalid_data(text, data_type):
            is_valid = False
            if data_type == Pallet:
                if len(text) == 4:
                    is_valid = True

            elif data_type == Trailer:
                if len(text) >= 2:
                    is_valid = True

            return is_valid

        @staticmethod
        def add_element_validator(records, element, elementT):
            element = Services.HelperMethods.filter_with_regex(element, elementT)
            is_valid = Services.HelperMethods.mark_invalid_data(element, elementT)
            is_valid = is_valid and Services.DatabaseMethods.mark_invalid_pk(
                element, elementT
            )
            records.append((element, is_valid))
            return records

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

        def mark_invalid_pk(element, elementT):
            try:
                object = db.session.get(elementT, element)
                return True if not object else False
            except OperationalError as e:
                logger.error(f"OperationalError: {e}")
                return False
            except SQLAlchemyError as e:
                logger.error(f"SQLAlchemyError: {e}")
                return False
