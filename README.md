TodosAPI - FastAPI
A REST API for managing personal to-do items, built with FastAPI and SQLAlchemy. The project was created to explore core FastAPI concepts such as routing, dependency injection, request validation with Pydantic, and JWT-based authentication.
Features
User registration and login with JWT authentication
Password hashing with bcrypt
Role-based access control (regular users vs admin)
Full CRUD operations on to-do items, scoped to the logged-in user
Admin endpoints for managing all to-do items across users
SQLite database via SQLAlchemy ORM
Tech Stack
FastAPI - web framework
SQLAlchemy - ORM
SQLite - database
Pydantic - request/response data validation
Passlib (bcrypt) - password hashing
python-jose - JWT token creation and validation
Uvicorn - ASGI server
Project Structure
```
.
├── main.py              # App entry point, includes all routers
├── models.py             # SQLAlchemy models (Users, Todos)
├── database.py            # Database connection and session setup
├── TodoRequest.py          # Pydantic schema for to-do requests
├── UserRequest.py          # Pydantic schemas for user requests and tokens
└── routers/
    ├── auth.py            # Registration, login, JWT handling
    ├── todos.py            # CRUD endpoints for to-do items
    ├── admin.py            # Admin-only endpoints
    └── users.py            # User profile and password management
```
Setup
Clone the repository and create a virtual environment:
```
python -m venv venv
venv\Scripts\activate
```
Install dependencies:
```
pip install -r requirements.txt
```
Run the application:
```
uvicorn main:app --reload
```
Open the interactive API docs at `http://127.0.0.1:8000/docs`
API Endpoints
Auth (`/auth`)
Method	Endpoint	Description
POST	`/auth/`	Registers a new user, hashes the password before storing it
POST	`/auth/token`	Authenticates a user and returns a JWT access token
GET	`/auth/users`	Returns a list of all registered users
Todos (`/`)
Method	Endpoint	Description
GET	`/`	Returns all to-do items belonging to the logged-in user
GET	`/{todo_id}`	Returns a single to-do item owned by the logged-in user
POST	`/todo`	Creates a new to-do item for the logged-in user
PUT	`/todo/{todo_id}`	Updates an existing to-do item owned by the logged-in user
DELETE	`/todo/{todo_id}`	Deletes a to-do item owned by the logged-in user
All endpoints require a valid JWT token and only operate on to-do items owned by the authenticated user.
Admin (`/admin`)
Method	Endpoint	Description
GET	`/admin/todo`	Returns all to-do items in the database, regardless of owner
DELETE	`/admin/todo/{todo_id}`	Deletes any to-do item by id
These endpoints require the authenticated user to have the `admin` role.
Users (`/users`)
Method	Endpoint	Description
GET	`/users/`	Returns the profile of the logged-in user
PUT	`/users/password`	Changes the password of the logged-in user, after verifying the current password
Authentication Flow
A user registers through `POST /auth/`.
The user logs in through `POST /auth/token` with their username and password, and receives a JWT access token.
The token is sent in the `Authorization` header as a Bearer token on every subsequent request.
Each protected endpoint decodes the token to identify the user and, where relevant, checks their role.
Notes
This project was built as a learning exercise, with a focus on understanding how the different parts of FastAPI fit together: routers, dependencies, database sessions, request/response models, and authentication.
