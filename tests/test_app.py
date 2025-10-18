import pytest
import os
import tempfile
import sys
from app.forms import CreateShipmentForm
from app.services import HelperMethods

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app, db


@pytest.fixture
def app():
    """Create application instance for testing."""
    test_app = create_app()

    db_fd, db_path = tempfile.mkstemp()
    test_app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    test_app.config["TESTING"] = True
    test_app.config["WTF_CSRF_ENABLED"] = False  # Disable CSRF for testing

    with test_app.app_context():
        db.create_all()
        yield test_app
        db.session.remove()
        db.drop_all()

    # Cleanup
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
        helper = HelperMethods()
        assert helper.boolean_to_status_string(True) == "At Capacity"
        assert helper.boolean_to_status_string(False) == "Not at Capacity"

    def test_remove_delimiters(self):
        """Test remove delimiters for functionality"""
        helper = HelperMethods()
        assert helper.remove_delimiters("8136-0025-2025") == "813600252025"
        assert helper.remove_delimiters("8136--0025--2025") == "813600252025"
        assert helper.remove_delimiters("8136 0025 2025") == "813600252025"
        assert helper.remove_delimiters("8136   0025-2025") == "813600252025"
        assert helper.remove_delimiters("8136/0025/2025") == "813600252025"

class TestCreateShipmentForm:
    """Test create shipment form for functionality"""
    def test_form_valid(self, app):
        """Test form validation with valid data."""
        with app.app_context():
            form = CreateShipmentForm(data={
                'registration_number': '8150-0939-2934',
                'first_name': 'John',
                'last_name': 'Doe',
                'tag_colour': 'Red',
                'tag_code': 'ABC123',
                'date_received': '2025-10-18 14:30:00',
                'date_out': '2025-10-19 09:00:00',
                'origin': 'Toronto',
                'destination': 'Ottawa',
                'driver_in': 'Mike',
                'driver_out': 'Sarah',
                'checked_in_by': 'John',
                'checked_out_by': 'Jane',
            })
            assert form.validate()

    def test_form_invalid(self, app):
        """Test form validation with invalid data"""
        with app.app_context():
            form = CreateShipmentForm(data={
                'registration_number': '',
                'first_name': 'John',
                'last_name': 'Doe',
                'tag_colour': 'Red',
                'tag_code': 'ABC123',
                'date_received': '2025-10-18 14:30:00',
                'date_out': '2025-10-19 09:00:00',
                'origin': 'Toronto',
                'destination': 'Ottawa',
                'driver_in': 'Mike',
                'driver_out': 'Sarah',
                'checked_in_by': 'John',
                'checked_out_by': 'Jane',
            })
            assert not form.validate()

    def test_form_requirements(self, app):
        """Test Non PK Field That Is Required"""
        with app.app_context():
            form = CreateShipmentForm(data={
                'registration_number': '',
                'first_name': 'John',
                'last_name': 'Doe',
                'tag_colour': 'Red',
                'tag_code': 'ABC123',
                'date_received': '2025-10-18 14:30:00',
                'date_out': '2025-10-19 09:00:00',
                'origin': '',
                'destination': 'Ottawa',
                'driver_in': 'Mike',
                'driver_out': 'Sarah',
                'checked_in_by': 'John',
                'checked_out_by': 'Jane',
            })
            assert not form.validate()

    def test_form_optional_field(self, app):
        """Test Non PK Field That Is Optional"""
        with app.app_context():
            form = CreateShipmentForm(data={
                'registration_number': '',
                'first_name': 'John',
                'last_name': 'Doe',
                'tag_colour': 'Red',
                'tag_code': 'ABC123',
                'date_received': '2025-10-18 14:30:00',
                'date_out': '2025-10-19 09:00:00',
                'origin': 'Toronto',
                'destination': '',
                'driver_in': 'Mike',
                'driver_out': 'Sarah',
                'checked_in_by': 'John',
                'checked_out_by': 'Jane',
            })
            assert not form.validate()




