import pytest
from flask import session
from app import app

@pytest.fixture
def client():
    """Fixture to create a test client for the Flask app."""
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test_secret'
    with app.test_client() as client:
        with app.app_context():
            yield client

def mock_api_responses(requests_mock):
    """Mock API responses."""
    requests_mock.post("http://localhost:3001/auth/login", json={
        "token": "mock_jwt_token",
        "role": "user"
    })
    requests_mock.get("http://localhost:3001/books", json={
        "books": [
            {"id": 1, "title": "Test Book", "author": "Author A", "borrowed": False},
            {"id": 2, "title": "Another Book", "author": "Author B", "borrowed": True}
        ]
    })
    requests_mock.post("http://localhost:3001/books/1/borrow", status_code=200)

# -----------------
# Test Cases
# -----------------

def test_home_redirects_to_login(client):
    """Test that the home route redirects to the login page."""
    response = client.get("/")
    assert response.status_code == 302
    assert b"login" in response.data

def test_user_login_successful(client, requests_mock):
    """Test a successful login."""
    mock_api_responses(requests_mock)

    response = client.post("/login", data={"username": "mario", "password": "rossi"})
    assert response.status_code == 302
    assert session.get('jwt_token') == "mock_jwt_token"

def test_admin_login_successful(client, requests_mock):
    """Test a successful login."""
    mock_api_responses(requests_mock)

    response = client.post("/login", data={"username": "admin", "password": "admin"})
    assert response.status_code == 302
    assert session.get('jwt_token') == "mock_jwt_token"

def test_login_failed(client, requests_mock):
    """Test a failed login."""
    requests_mock.post("http://localhost:3001/auth/login", status_code=404, json={"message": "Invalid credentials. Please try again."})

    response = client.post("/login", data={"username": "wrong", "password": "pass"})
    assert response.status_code == 200
    assert b"Invalid credentials" in response.data

def test_books_list(client, requests_mock):
    """Test fetching the list of books."""
    mock_api_responses(requests_mock)

    with client.session_transaction() as session:
        session['jwt_token'] = "mock_jwt_token"

    response = client.get("/books")
    assert response.status_code == 200
    assert b"Test Book" in response.data

def test_book_borrow(client, requests_mock):
    """Test borrowing a book."""
    mock_api_responses(requests_mock)

    with client.session_transaction() as session:
        session['jwt_token'] = "mock_jwt_token"

    response = client.post("/books", data={"book_id": "1", "action": "borrow"})
    assert response.status_code == 302
    assert b"Book borrowed successfully!" in response.data

def test_admin_access(client, requests_mock):
    """Test admin functionality (add, edit, delete)."""
    mock_api_responses(requests_mock)

    with client.session_transaction() as session:
        session['jwt_token'] = "mock_jwt_token"

    # Simulate adding a book
    requests_mock.post("http://localhost:3001/books", status_code=201)
    response = client.post("/admin", data={"action": "add", "title": "New Book", "author": "Admin"})
    assert response.status_code == 302
    assert b"Action completed successfully." in response.data

    # Simulate editing a book
    requests_mock.put("http://localhost:3001/books/1", status_code=200)
    response = client.post("/admin", data={"action": "edit", "book_id": "1", "title": "Updated Book", "author": "Admin"})
    assert response.status_code == 302
    assert b"Action completed successfully." in response.data

    # Simulate deleting a book
    requests_mock.delete("http://localhost:3001/books/1", status_code=200)
    response = client.post("/admin", data={"action": "delete", "book_id": "1"})
    assert response.status_code == 302
    assert b"Action completed successfully." in response.data
