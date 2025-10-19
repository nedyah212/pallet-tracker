from . import db
from .logging import logger
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError

class Services():

  class HelperMethods():

    def boolean_to_status_string(self, boolean):
      return "At Capacity" if boolean else "Not at Capacity" if boolean is not None else ''

    @staticmethod
    def remove_delimiters(text):
      return text.replace('-', '').replace(' ', '').replace('/', '') if text is not None else ''

  class DatabaseMethods():

    def create_shipment(shipment):
      try:
          db.session.add(shipment)
          db.session.commit()
          logger.info(f"Success: {shipment} has been added to the database.")

      except IntegrityError as e:
          logger.error(f"IntegrityError: {e}")
          db.session.rollback()
      except OperationalError as e:
          logger.error(f"OperationalError: {e}")
          db.session.rollback()
      except SQLAlchemyError as e:
          logger.error(f"SQLAlchemyError: {e}")
          db.session.rollback()