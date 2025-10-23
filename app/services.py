from . import db
from .logging import logger
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError
from .models import Shipment


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
