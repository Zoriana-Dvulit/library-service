# Library-service

### This Django project was created for managing system for book borrowings in Library Service!

This project implements a Library Service with CRUD functionality, JWT token authentication,
and permissions that allow only admin users to create/update/delete books.

All users, including unauthenticated ones, can list books.

The project also includes a Users Service with JWT support, and a Borrowings Service that manages borrowings based on
user expectations for book reading time.

The project also implements filtering for the Borrowings List endpoint, allowing non-admin users to see only their own
borrowings,
and admin users to see all borrowings or only those for a specific user.

Returning a borrowing increases the book's inventory by one, and borrowers cannot return a book twice.

## Installation

Python must be already installed

```shell
git clone https://github.com/Zoriana-Dvulit/library-service.git
cd library-service
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver #starts Django Server
```


## Environment Variables

This project uses environment variables to store sensitive information. To set up the environment variables:

1. Copy the `.env_sample` file and rename it to `.env`.
2. Replace the sample values in the `.env` file with your actual values.

## Register

To register a new user, make a POST request to the `register` endpoint with the following data:
```POST /api/register/

{
"username": "your_username",
"email": "your_email@example.com",
"password": "your_password"
}
```

The API will create a new user with the provided username, email, and password. 
The response will include the registered user's details and a success message.

## Test User Credentials:
- Username: testuser
- Email: testuser@example.com
- Password: testpassword


### Registration via Token

Alternatively, you can also register a user using a token-based authentication system. 
After registering, you can obtain an access token by making a POST request to the 
`token_obtain_pair` endpoint with the user's login credentials (username and password). 
The response will include an access token and a refresh token, which can be used for subsequent authenticated requests.

## Data load

To load test data, use the following command: 
```shell
python manage.py loaddata fixture_data.json
```

## Features

* Authentication functionality for User
* Managing books directly from website interface
* Managing borrowings based on User's days to read the book
* Powerful admin panel for advanced managing
