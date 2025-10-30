from .. import db
from ..logging import logger
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError
from ..models import Shipment


class ShipmentRepository:

    @staticmethod
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

    @staticmethod
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
            db.session.merge(record)
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

    @staticmethod
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
