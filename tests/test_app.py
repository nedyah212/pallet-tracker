import pytest
import os
import tempfile
import sys
from app.models import Shipment, Pallet, Trailer, OversizedGood
from app.controllers import ShipmentsController, SettingsController
from app.services import StorageServices
from app.forms import (
    EditTypeForm,
    EditSettingForm,
    BatchEntryForm,
    EditTypeFloorForm,
    EditTypeTrailerForm,
    CreateShipmentForm,
)

from app.repositories import ShipmentRepository

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
    test_app.config["SECRET_KEY"] = "test-secret-key-for-testing"

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

    def test_add_element(self, app):
        """Test functionality of add element"""
        with app.app_context():
            msg, category = StorageServices.add_element("1001", Pallet)
            assert msg == "Valid Pallet: 1001"
            msg, category = StorageServices.add_element("1001", Pallet)
            assert msg == "Invalid Pallet: 1001"


class TestCreateShipmentForm:
    """Test create shipment form for functionality"""

    def test_form_valid(self, app):
        """Test form validation with valid data."""
        with app.app_context():
            form = CreateShipmentForm(
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
            form = CreateShipmentForm(
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
            form = CreateShipmentForm(
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
            form = CreateShipmentForm(
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
            form = CreateShipmentForm(
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
    def test_update(self, app):
        """Test functionality of update"""
        with app.app_context():
            pallet = Pallet(id="1000")
            ShipmentRepository.update(pallet)
            assert len(db.session.query(Pallet).all()) == 1

    def test_get_shipment(self, app):
        """Test functionality of get shipment"""
        with app.app_context():
            id = "8132025"
            shipment = Shipment(registration_number=id, first_name="1", last_name="2")
            db.session.add(shipment)
            db.session.commit()

            assert ShipmentRepository.get_shipment(id) == shipment

    def mark_invalid_pk(self, app):
        """Test functionality of mark invlalid pk"""
        with app.app_context():
            helper = ShipmentRepository.DatabaseMethods()
            assert helper.mark_invalid_pk("1001", Pallet) == True
            assert helper.mark_invalid_pk("100", Pallet) == False
            assert helper.mark_invalid_pk("", Pallet) == False
            assert helper.mark_invalid_pk("T100", Trailer) == True
            assert helper.mark_invalid_pk("T", Trailer) == False
            assert helper.mark_invalid_pk("", Pallet) == False
