import pytest
from flask import session
import sys
sys.path.append('.')
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
            {"id": 1, "title": "Test Book", "author": "Author A", "is_borrowed": False},
            {"id": 2, "title": "Another Book", "author": "Author B", "is_borrowed": True}
        ]
    })
    requests_mock.post("http://localhost:3001/books/1/borrow", status_code=200)
    requests_mock.post("http://localhost:3001/books/2/return", status_code=200)

# -----------------
# Test Cases
# -----------------

def test_home_redirects_to_login(client):
    """Test that the home route redirects to the login page."""
    #act
    response = client.get("/")

    #assert
    assert response.status_code == 302
    assert b"login" in response.data

def test_user_login_successful(client, requests_mock):
    """Test a successful login."""
    #arrange
    mock_api_responses(requests_mock)

    #act
    response = client.post("/login", data={"username": "mario", "password": "rossi"})

    #assert
    assert response.status_code == 302
    assert session.get('jwt_token') == "mock_jwt_token"

def test_admin_login_successful(client, requests_mock):
    """Test a successful login."""
    #arrange
    mock_api_responses(requests_mock)

    response = client.post("/login", data={"username": "admin", "password": "admin"})
    assert response.status_code == 302
    assert session.get('jwt_token') == "mock_jwt_token"

def test_books_list(client, requests_mock):
    """Test fetching the list of books."""
    mock_api_responses(requests_mock)

    with client.session_transaction() as session:
        session['jwt_token'] = "mock_jwt_token"

    response = client.get("/books")
    assert response.status_code == 200

def test_book_borrow(client, requests_mock):
    """Test borrowing a book."""
    mock_api_responses(requests_mock)

    with client.session_transaction() as session:
        session['jwt_token'] = "mock_jwt_token"

    response = client.post("/books", data={"book_id": "1", "action": "borrow"})
    assert response.status_code == 302

def test_book_return(client, requests_mock):
    """Test borrowing a book."""
    mock_api_responses(requests_mock)

    with client.session_transaction() as session:
        session['jwt_token'] = "mock_jwt_token"

    response = client.post("/books", data={"book_id": "2", "action": "return"})
    assert response.status_code == 302

def test_admin_add(client, requests_mock):
    """Test admin add functionality"""
    mock_api_responses(requests_mock)

    with client.session_transaction() as session:
        session['jwt_token'] = "mock_jwt_token"

    # Simulate adding a book
    requests_mock.post("http://localhost:3001/books", status_code=200)
    response = client.post("/books", data={"action": "add", "title": "New Book", "author": "Admin"})
    assert response.status_code == 302

def test_admin_edit(client, requests_mock):
    """Test admin edit functionality"""
    mock_api_responses(requests_mock)

    with client.session_transaction() as session:
        session['jwt_token'] = "mock_jwt_token"

    # Simulate editing a book
    requests_mock.put("http://localhost:3001/books/1", status_code=200)
    response = client.post("/books", data={"action": "edit", "book_id": "1", "title": "Updated Book", "author": "Admin"})
    assert response.status_code == 302

def test_admin_delete(client, requests_mock):
    """Test admin delete functionality"""
    mock_api_responses(requests_mock)

    with client.session_transaction() as session:
        session['jwt_token'] = "mock_jwt_token"

    # Simulate deleting a book
    requests_mock.delete("http://localhost:3001/books/1", status_code=200)
    response = client.post("/books", data={"action": "delete", "book_id": "1"})
    assert response.status_code == 302
