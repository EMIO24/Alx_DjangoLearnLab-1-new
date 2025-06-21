# Advanced API Project - Book Views

This project demonstrates the use of Django REST Framework's generic views for CRUD operations on the Book model.

## Endpoints

* **GET /api/books/**: Retrieves a list of all books (public).
* **GET /api/books/{id}/**: Retrieves a single book by ID (public).
* **POST /api/books/create/**: Creates a new book (requires authentication).
* **PUT/PATCH /api/books/{id}/update/**: Updates an existing book (requires authentication).
* **DELETE /api/books/{id}/delete/**: Deletes a book (requires authentication).

## Permissions

* Read-only access is allowed for all users.
* Create, update, and delete operations require authentication.