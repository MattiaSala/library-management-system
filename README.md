# Library Management System

This is a Flask-based Library Management System where users can log in, manage books (borrow, return, add, edit, delete), and perform authentication with JWT (JSON Web Token). It interacts with a Mock API to manage book data, ensuring the user can only perform actions if they are logged in.

## Features

- **User Authentication**: Users can log in with a username and password, and the system uses JWT for secure session management.
- **Book Management**: 
  - View the list of books
  - Borrow and return books
  - Add new books to the collection
  - Edit book details
  - Delete books from the system
- **Role-based access**: User roles are handled through JWT tokens to define what actions are permissible.
  
## Technologies Used

- **Flask**: A Python micro-framework used for building the web app.
- **JWT**: For secure authentication.
- **Mock API**: A simulated backend (using Mockoon or another mock API tool) to handle book data.
- **HTML**: For frontend rendering of pages (login and books management).

## Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.10.6
- Flask
- Requests
- A running Mock API server (e.g., Mockoon)

To install the required Python packages, run:

```bash
pip install -r requirements.txt
```

## 🚀 Usage

Make sure you have [npx](https://www.npmjs.com/package/npx) installed (`npx` is shipped by default since npm `5.2.0`)

Just run the following command at the root of your project and answer questions:

```sh
npx readme-md-generator
```

Or use default values for all questions (`-y`):

```sh
npx readme-md-generator -y
```

Use your own `ejs` README template (`-p`):

```sh
npx readme-md-generator -p path/to/my/own/template.md
```

You can find [ejs README template examples here](https://github.com/kefranabg/readme-md-generator/tree/master/templates).

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
Put here all the assumptions...


## Author

👤 **Mattia Sala**

- X: [@iammattsala](https://twitter.com/iammattsala)
- Github: [@MattiaSala](https://github.com/MattiaSala)

## 📝 License

Copyright © 2019 [Mattia Sala](https://github.com/MattiaSala).<br />
This project is [MIT](https://github.com/kefranabg/readme-md-generator/blob/master/LICENSE) licensed.


