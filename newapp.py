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
API_BASE_URL = "http://localhost:3001"  # Replace with your Mockoon API URL

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
        #print(f"The response is ---> {response.text}")
        #print(f"The response STATUS CODE is ---> {response.status_code}, {type(response.status_code)}")
        #print(f"RESPONSE:\n{response.json()}")
        if response.status_code == 200:
            session['jwt_token'] = response.json().get('token')
            #flash("Login successful!", "success")
            session['role'] = response.json().get('role')

            return redirect(url_for('books'))
        else:
            print(response.status_code)
            message = response.json()["message"]
            #print("Invalid credentials. Please try again.")
            #flash("Invalid credentials. Please try again.", "error")
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
    """Manage books: Borrow, Return, Add, Edit, Delete."""
    if 'jwt_token' not in session:
        flash("You need to log in first.", "warning")
        return redirect(url_for('login'))

    # Fetch books list
    """if request.method == "GET":
        response = requests.get(f"{API_BASE_URL}/books", headers=get_headers())
        print("GET /books\-----------------n\n")
        print(f"IN BOOKS RESPONSE TEXT --->{response.text}")
        print(f"IN BOOKS RESPONSE CODE --->{response.status_code}")

        books = response.json() if response.status_code == 200 else []"""
    print("------------ EGG --------")
    response = requests.get(f"{API_BASE_URL}/books", headers=get_headers())
    print("GET /books\-----------------n\n")
    print(f"IN BOOKS RESPONSE TEXT --->{response.text}")
    print(f"IN BOOKS RESPONSE CODE --->{response.status_code}")

    #books = response.json() if response.status_code == 200 else []
    books = json.loads(response.text) if response.status_code == 200 else []
    print(f"BOOKS ==> {books[0]}")
    #elif request.method == "POST":
    if request.method == "POST":
        action = request.form['action']

        # Handle Borrow and Return
        if action in ["borrow", "return"]:
            book_id = request.form['book_id']
            endpoint = f"{API_BASE_URL}/books/{book_id}/{action}"
            response = requests.post(endpoint, headers=get_headers())
            print("POST /books/id/borrow\n-----------------\n")

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
            response = requests.post(f"{API_BASE_URL}/books", json=data, headers=get_headers())
            #print("POST /books/id/ (add)\n-----------------\n")

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
            #print(f"DELETING BOOK with ID --> {book_id}\n\n")
            response = requests.delete(f"{API_BASE_URL}/books/{book_id}", headers=get_headers())
            #print("DELETE /books/id/ (delete)\n-----------------\n")
            #print(f"DELETE RESPONSE TEXT --->{response.text}")
            #print(f"DELETE RESPONSE CODE --->{response.status_code}")
            #message = response.json()["message"]
            
            if response.status_code == 200:
                #flash(message,"success")
                flash("Book deleted successfully!", "success")
            else:
                #flash(message,"error")
                #print("An error occurred while deleting the book.")
                flash(response.json().get('message', 'An error occurred while deleting the book.'), "error")

        return redirect(url_for('books'))
    
    return render_template("books.html", books=books)
    #return render_template("books.html", books=books['books'])



# -----------------
# Run Application
# -----------------
if __name__ == "__main__":
    app.run(debug=True)