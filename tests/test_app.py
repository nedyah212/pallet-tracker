import pytest
import os
import tempfile
import sys

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
