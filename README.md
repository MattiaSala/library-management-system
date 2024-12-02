# Library Management System

This is a Flask-based Library Management System where users can log in, manage books (borrow, return, add, edit, delete), and perform authentication with JWT (JSON Web Token). It interacts with a Mock API to manage book data, ensuring the user can only perform actions if they are logged in and based on their roles.

## Features

- **User Authentication**: Users can log in with a username and password, and the system uses JWT for secure session management.
- **Book Management**: 
  - View the list of books
  - Borrow and return books
  - Add new books to the collection
  - Edit book details
  - Delete books from the system
- **Role-based access**: User roles are handled to define what actions are permissible.
  
## Technologies Used

- **Flask**: A Python framework used for building the web app.
- **JWT**: For secure authentication.
- **Mockoon**: A simulated backend to mock API calls.
- **PyTest**: Python library for performing Unit-tests.
- **HTML and TailwindCSS**: For frontend rendering of pages (login and books management).

## Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.10.X
- Flask
- Requests
- A running Mock API server (e.g., Mockoon)


##  Usage
### Run the Backend
To run the backend:
1. Open **Mockoon**
2. File > Open local enviroment
3. Select the `v5.json` file contained in the `./backend-config` folder
4. Start the server


### Run Locally
To run the Flask application locally:

0. Clone the repository:
```bash
git clone https://github.com/MattiaSala/library-management-system.git

cd library-management-system
```

1. Create a Virtual enviroment `venv` and activate it:
```bash
venv -m venv venv

venv\Scripts\Activate.ps1 # if using Windows Powershell

source ./venv/bin/activate # if using Linux or MacOS

```


2. Install requirements from the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

3. To run the Flask application use:
 ```bash
flask --app app run
```

4. Open the web browser at:
```bash
http://localhost:5000
```

### 🐋 Use Docker
To run the application using Docker:
1. Go to the `app.py` file and put your local machine `ip address` in `API_BASE_URL` with the correct port of the Mockoon server.

2. Build Docker image
 ```bash
docker build -t flask-app .
```

3. Run container in detached mode
 ```bash
docker run -d -p 5000:5000 --name flask-container flask-app
```

4. Open app in web browser
 ```bash
http://<your-ip-address>:5000
```


## Run the unit tests
To run the unit tests digit in the terminal:
```sh
pytest tests\test.py
```
The unit tests are provided for:
- Authentication
- Borrowing of a book 
- Returning of a borrowed book 
- Add of a new book
- Edit of a new book
- Delete of a new book

## Assumptions
### Users
The users are simulated with rules in Mockoon. The users are:
`username = mario` and `password = rossi` which has `user` permissions: Borrow and Return.
`username = admin` and `password = admin` which has `admin` permissions: Borrow, Return, Add, Edit, Delete.

### Endpoints
- `ALL /*`
- `POST /auth/login`
- `CRUD /books`
  - `GET /books`: list all the books
  - `POST /books` : to simulate the adding of a new book
  - `PUT /books/:id`: to simulate the edit of a book
  - `DELETE /books/:id`: to simulate the deletion of a book
  
  CRUD operations are mocked in the backend by making use of "CRUD routes" of Mockoon that handles the data of Book databucket automatically. (For more details on how Mockoon manages the CRUD operations: )

- `POST /books/:id/borrow`: borrowing of a book
- `POST /books/:id/return`: returning of a borrowed book.


## Author

👤 **Mattia Sala**
- Github: [@MattiaSala](https://github.com/MattiaSala)
