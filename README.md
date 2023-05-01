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

## Features

* Authentication functionality for User
* Managing books directly from website interface
* Managing borrowings based on User's days to read the book
* Powerful admin panel for advanced managing

