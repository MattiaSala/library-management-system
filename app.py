from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask import flash
from flask import jsonify
import requests
import json


app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Mock API base URL
API_BASE_URL = "http://localhost:3001" 

print(API_BASE_URL)
# -----------------
# Helper Functions
# -----------------

def get_headers():
    """Get headers for authenticated requests."""
    token = session.get('jwt_token')
    print(f"TOKEN: {token}")
    if not token:
        return {}
    return {'Authorization': f'Bearer {token}'}

# -----------------
# Routes
# -----------------

@app.route("/")
def home():
    """Homepage redirecting to login."""
    if 'jwt_token' in session:
        return redirect(url_for('books'))
    return redirect(url_for('login'))

@app.route("/login", methods=["GET", "POST"])
def login():
    """User login."""
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        response = requests.post(f"{API_BASE_URL}/auth/login", json={'username': username, 'password': password})

        if response.status_code == 200:
            session['jwt_token'] = response.json().get('token')
            session['role'] = response.json().get('role')

            return redirect(url_for('books'))
        else:
            print(response.status_code)
            message = response.json()["message"]
            flash(message, "error")
    return render_template("login.html")

@app.route("/logout", methods=["POST"])
def logout():
    """User logout."""
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for('login'))

@app.route("/books", methods=["GET", "POST", "PUT", "DELETE"])
def books():
    """
    Manage books for both normal user and admin user.
    The normal user can: Borrow and Return. The admin can: Borrow, Return, Add, Edit, Delete.
    """
    if 'jwt_token' not in session:
        flash("You need to log in first.", "warning")
        return redirect(url_for('login'))

    # Fetch books list
    response = requests.get(f"{API_BASE_URL}/books", headers=get_headers())

    books = json.loads(response.text) if response.status_code == 200 else []

    if request.method == "POST":
        action = request.form['action']

        # Handle Borrow and Return
        if action in ["borrow", "return"]:
            book_id = request.form['book_id']
            endpoint = f"{API_BASE_URL}/books/{book_id}/{action}"
            response = requests.post(endpoint, headers=get_headers())

            if response.status_code == 400:
                flash(f"Book already {action}ed!", "error")
            elif response.status_code == 200:
                flash(f"Book {action}ed successfully!", "success")
            else:
                flash(response.json().get('message', 'An error occurred.'), "error")

        # Handle Add
        elif action == "add":
            data = {
                "title": request.form['title'],
                "author": request.form['author'],
                "is_borrowed": False
            }
            print(data["title"])
            print(f"BOOKS:\n{books}")
            
            if any(book['title'] == data["title"] and book['author'] == data["author"] for book in books):
                flash("Book already in library!")
            else:
                response = requests.post(f"{API_BASE_URL}/books", json=data, headers=get_headers())

                if response.status_code in [200, 201]:
                    flash("Book added successfully!", "success")
                else:
                    flash(response.json().get('message', 'An error occurred while adding the book.'), "error")

        # Handle Edit
        elif action == "edit":
            book_id = request.form['book_id']
            data = {
                "title": request.form['title'],
                "author": request.form['author'],
                "is_borrowed": request.form.get('borrowed', 'false') == 'true'
            }

            if data["is_borrowed"] == 'true':
                flash("Cannot edit a borrowed book", "error")
            else:
                response = requests.put(f"{API_BASE_URL}/books/{book_id}", json=data, headers=get_headers())
                #print("PUT /books/id/ (edit)\n-----------------\n")

                if response.status_code == 200:
                    flash("Book updated successfully!", "success")
                else:
                    flash(response.json().get('message', 'An error occurred while updating the book.'), "error")

        # Handle Delete
        elif action == "delete":
            book_id = request.form['book_id']
            response = requests.delete(f"{API_BASE_URL}/books/{book_id}", headers=get_headers())

            
            if response.status_code == 200:
                flash("Book deleted successfully!", "success")
            else:
                flash(response.json().get('message', 'An error occurred while deleting the book.'), "error")

        return redirect(url_for('books'))
    
    return render_template("books.html", books=books)


# -----------------
# Run Application
# -----------------
if __name__ == "__main__":
    app.run(debug=True)