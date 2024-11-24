import pytest
from app import app

@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test_secret_key'
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_session(client):
    """Set up a mock session for authenticated tests."""
    with client.session_transaction() as sess:
        sess['jwt_token'] = 'test_jwt_token'
        sess['role'] = 'admin'

# --------------------
# Mock Data and Helpers
# --------------------

BOOKS_API_RESPONSE = [
    {"id": 1, "title": "Book 1", "author": "Author 1", "is_borrowed": False},
    {"id": 2, "title": "Book 2", "author": "Author 2", "is_borrowed": True},
]

def mock_get_books(*args, **kwargs):
    """Mocked GET request for /books."""
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    return MockResponse(BOOKS_API_RESPONSE, 200)


# --------------------
# Tests
# --------------------

def test_home_redirect(client):
    """Test if the home route redirects to login when not logged in."""
    response = client.get("/")
    assert response.status_code == 302
    assert "/login" in response.location

def test_login_get(client):
    """Test if the login page is accessible."""
    response = client.get("/login")
    assert response.status_code == 200
    assert b"Login" in response.data

def test_books_unauthenticated(client):
    """Test access to the books page when unauthenticated."""
    response = client.get("/books")
    assert response.status_code == 302
    assert "/login" in response.location

@pytest.mark.parametrize(
    "endpoint, method, data, status_code",
    [
        ("/login", "POST", {"username": "admin", "password": "password"}, 200),
        ("/books", "POST", {"action": "action"...})
    ...)).-> `
