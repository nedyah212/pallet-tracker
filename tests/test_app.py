import pytest
import os
import tempfile
import sys
from app.forms import Forms
from app.services import Services
from app.models import Shipment, Pallet, Trailer
from flask import get_flashed_messages
from app.controllers import Controller

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app, db


@pytest.fixture
def app():
    """Create application instance for testing."""
    test_app = create_app()

    db_fd, db_path = tempfile.mkstemp()
    test_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    test_app.config["TESTING"] = True
    test_app.config["WTF_CSRF_ENABLED"] = False

    with test_app.app_context():
        db.create_all()
        yield test_app
        db.session.remove()
        db.drop_all()

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """Create a test client."""
    return app.test_client()


class TestHomePage:
    """Test the home page and basic functionality."""

    def test_home_page_loads(self, client):
        """Test that the home page loads successfully."""
        response = client.get("/")
        assert response.status_code == 200
        assert b"<!DOCTYPE html>" in response.data or b"<html" in response.data


class TestHelperMethods:
    """Test helper functions for functionality"""

    def test_boolean_to_status_string(self):
        """Test method for satisfactory functionality"""
        helper = Services.HelperMethods()
        assert helper.boolean_to_status_string(True) == "At Capacity"
        assert helper.boolean_to_status_string(False) == "Not at Capacity"
        assert helper.boolean_to_status_string(None) == ""

    def test_remove_delimiters(self):
        """Test remove delimiters for functionality"""
        helper = Services.HelperMethods()
        assert helper.remove_delimiters("8136-0025-2025") == "813600252025"
        assert helper.remove_delimiters("8136--0025--2025") == "813600252025"
        assert helper.remove_delimiters("8136 0025 2025") == "813600252025"
        assert helper.remove_delimiters("8136   0025-2025") == "813600252025"
        assert helper.remove_delimiters("8136/0025/2025") == "813600252025"
        assert helper.remove_delimiters(None) == ""

    def test_filter_with_regex(self):
        """Test filter with regex for functionality"""
        helper = Services.HelperMethods()
        assert helper.filter_with_regex("!%^*&$8 72d30874)*&(*^(&%)),") == "87230874,"
        assert helper.filter_with_regex("(*^&%^T55 92/,'[]k,", "trailer") == "T5592,k,"

    def test_batch_elements(self):
        """Test batch elements for functionality"""
        helper = Services.HelperMethods()
        assert len(helper.batch_get_elements("1006, %1002")) == 2
        assert len(helper.batch_get_elements(",1006, %1002, ,")) == 2
        assert len(helper.batch_get_elements("T204, T392, /X20", "trailer")) == 3

    def test_add_element(self, app):
        """Test of functionality for add_element"""

        # FIRST SECTION - with PK violation
        with app.test_request_context():
            elements = "1000,1001,1002"
            pallet = Pallet(id="1000")
            db.session.add(pallet)
            db.session.commit()

            msg = Controller.add_element(elements, type="pallet")
            message, category = msg
            assert message == "Failed to add pallet(s): 1000"
            assert len(db.session.query(Pallet).all()) == 1

        # SECOND SECTION - successful add
        with app.test_request_context():
            db.session.query(Pallet).delete()
            db.session.commit()
            assert len(db.session.query(Pallet).all()) == 0

            msg = Controller.add_element(elements, type="pallet")
            assert msg == ""
            assert len(db.session.query(Pallet).all()) == 3


class TestCreateShipmentForm:
    """Test create shipment form for functionality"""

    def test_form_valid(self, app):
        """Test form validation with valid data."""
        with app.app_context():
            form = Forms.CreateShipmentForm(
                data={
                    "registration_number": "815009392934",
                    "first_name": "John",
                    "last_name": "Doe",
                    "tag_colour": "Red",
                    "tag_code": "ABC123",
                    "date_received": "2025-10-18 14:30:00",
                    "date_out": "2025-10-19 09:00:00",
                    "origin": "Toronto",
                    "destination": "Ottawa",
                    "driver_in": "Mike",
                    "driver_out": "Sarah",
                    "checked_in_by": "John",
                    "checked_out_by": "Jane",
                }
            )
            assert form.validate()

    def test_form_invalid(self, app):
        """Test form validation with invalid data"""
        with app.app_context():
            form = Forms.CreateShipmentForm(
                data={
                    "registration_number": "",
                    "first_name": "John",
                    "last_name": "Doe",
                    "tag_colour": "Red",
                    "tag_code": "ABC123",
                    "date_received": "2025-10-18 14:30:00",
                    "date_out": "2025-10-19 09:00:00",
                    "origin": "Toronto",
                    "destination": "Ottawa",
                    "driver_in": "Mike",
                    "driver_out": "Sarah",
                    "checked_in_by": "John",
                    "checked_out_by": "Jane",
                }
            )
            assert not form.validate()

    def test_form_requirements(self, app):
        """Test Non PK Field That Is Required"""

        with app.app_context():
            form = Forms.CreateShipmentForm(
                data={
                    "registration_number": "",
                    "first_name": "John",
                    "last_name": "Doe",
                    "tag_colour": "Red",
                    "tag_code": "ABC123",
                    "date_received": "2025-10-18 14:30:00",
                    "date_out": "2025-10-19 09:00:00",
                    "origin": "",
                    "destination": "Ottawa",
                    "driver_in": "Mike",
                    "driver_out": "Sarah",
                    "checked_in_by": "John",
                    "checked_out_by": "Jane",
                }
            )
            assert not form.validate()

    def test_form_optional_field(self, app):
        """Test Non PK Field That Is Optional"""
        with app.app_context():
            form = Forms.CreateShipmentForm(
                data={
                    "registration_number": "",
                    "first_name": "John",
                    "last_name": "Doe",
                    "tag_colour": "Red",
                    "tag_code": "ABC123",
                    "date_received": "2025-10-18 14:30:00",
                    "date_out": "2025-10-19 09:00:00",
                    "origin": "Toronto",
                    "destination": "",
                    "driver_in": "Mike",
                    "driver_out": "Sarah",
                    "checked_in_by": "John",
                    "checked_out_by": "Jane",
                }
            )
            assert not form.validate()

    def test_form_submit(self, app, client):
        """Test Post, And For PK Violations"""
        with app.app_context():
            form = Forms.CreateShipmentForm(
                data={
                    "registration_number": "813601602025",
                    "first_name": "John",
                    "last_name": "Doe",
                    "tag_colour": "Red",
                    "tag_code": "ABC123",
                    "date_received": "2025-10-18 14:30:00",
                    "date_out": "2025-10-19 09:00:00",
                    "origin": "Toronto",
                    "destination": "Ottawa",
                    "driver_in": "Mike",
                    "driver_out": "Sarah",
                    "checked_in_by": "John",
                    "checked_out_by": "Jane",
                }
            )
            response = client.post(
                "/create_shipment", data=form.data, follow_redirects=True
            )
            assert response.status_code == 200


class TestDatabaseMethods:
    """Test functionality of DatabaseMethods"""

    def test_validate_element(self, app):
        """Test of functionality for validate element"""
        with app.app_context():
            pallet = Pallet(id="1001")
            trailer = Trailer(id="T2000")
            db.session.add(pallet)
            db.session.add(trailer)
            db.session.commit()

            helper = Services.DatabaseMethods()
            pallet1 = helper.validate_element("1001")
            pallet2 = helper.validate_element("1002")
            trailer1 = helper.validate_element("T2000", "trailer")
            trailer2 = helper.validate_element("T2002", "trailer")

            assert pallet1 is False
            assert pallet2 is True
            assert trailer1 is False
            assert trailer2 is True

    def test_update(self, app):
        """Test functionality of update"""
        with app.app_context():
            pallet = Pallet(id="1000")
            Services.DatabaseMethods.update(pallet)
            assert len(db.session.query(Pallet).all()) == 1

    def test_get_shipment(self, app):
        """Test functionality of update"""
        with app.app_context():
            id = "8132025"
            shipment = Shipment(registration_number=id, first_name="1", last_name="2")
            db.session.add(shipment)
            db.session.commit()

            assert Services.DatabaseMethods.get_shipment(id) == shipment
