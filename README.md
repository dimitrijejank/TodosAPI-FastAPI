TodosAPI - FastAPI
A full-stack to-do application built with FastAPI, SQLAlchemy, and PostgreSQL, with a server-rendered frontend using Jinja2 templates and Bootstrap. The project was created to explore core FastAPI concepts such as routing, dependency injection, request validation with Pydantic, JWT-based authentication, database migrations, and automated testing.
Features
User registration and login with JWT authentication
Password hashing with bcrypt
Role-based access control (regular users vs admin)
Full CRUD operations on to-do items, scoped to the logged-in user
Admin endpoints for managing all to-do items across users
User profile management, including password and phone number updates
PostgreSQL database via SQLAlchemy ORM
Database migrations with Alembic
Server-rendered frontend with Jinja2 templates and Bootstrap
Automated tests with pytest, run against a dedicated test database
Environment-based configuration, keeping database credentials out of the codebase
Tech Stack
FastAPI - web framework
SQLAlchemy - ORM
PostgreSQL - database
Alembic - database migrations
Pydantic - request/response data validation
Passlib (bcrypt) - password hashing
python-jose - JWT token creation and validation
Jinja2 - server-side templating
Bootstrap - frontend styling
pytest - automated testing
python-dotenv - environment variable management
Uvicorn - ASGI server
Project Structure
```
.
├── main.py                  # App entry point, includes all routers
├── models.py                 # SQLAlchemy models (Users, Todos)
├── database.py                # Database connection and session setup
├── TodoRequest.py              # Pydantic schema for to-do requests
├── UserRequest.py              # Pydantic schemas for user requests and tokens
├── alembic/                   # Database migration scripts
├── routers/
│   ├── auth.py                # Registration, login, JWT handling, login/register pages
│   ├── todos.py                # CRUD endpoints for to-do items, to-do pages
│   ├── admin.py                # Admin-only endpoints
│   └── users.py                # User profile and password management
├── templates/
│   ├── layout.html              # Shared page layout
│   ├── login.html               # Login form
│   ├── register.html             # Registration form
│   ├── todo.html                # List of the user's to-do items
│   ├── add-todo.html             # Form for creating a new to-do item
│   └── edit-todo.html            # Form for editing an existing to-do item
├── static/
│   ├── css/
│   └── js/
├── test/
│   └── test_todos.py             # Automated tests
├── .env                       # Environment variables (not committed)
└── requirements.txt
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
Create a `.env` file in the project root with your database connection strings:
```
DATABASE_URL=postgresql://username:password@localhost/TodoApplicationDatabase
TEST_DATABASE_URL=postgresql://username:password@localhost/TestDatabase
```
Run database migrations:
```
alembic upgrade head
```
Run the application:
```
uvicorn main:app --reload
```
Open the interactive API docs at `http://127.0.0.1:8000/docs`, or visit `http://127.0.0.1:8000/auth/login-page` for the web interface.
API Endpoints
Auth (`/auth`)
Method	Endpoint	Description
POST	`/auth/`	Registers a new user, hashes the password before storing it
POST	`/auth/token`	Authenticates a user and returns a JWT access token
GET	`/auth/users`	Returns a list of all registered users
Todos (`/todos`)
Method	Endpoint	Description
GET	`/todos/`	Returns all to-do items belonging to the logged-in user
GET	`/todos/{todo_id}`	Returns a single to-do item owned by the logged-in user
POST	`/todos/todo`	Creates a new to-do item for the logged-in user
PUT	`/todos/todo/{todo_id}`	Updates an existing to-do item owned by the logged-in user
DELETE	`/todos/todo/{todo_id}`	Deletes a to-do item owned by the logged-in user
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
PUT	`/users/phone_number`	Updates the phone number of the logged-in user
Authentication Flow
A user registers through `POST /auth/`.
The user logs in through `POST /auth/token` with their username and password, and receives a JWT access token.
For API usage, the token is sent in the `Authorization` header as a Bearer token on every subsequent request.
For the web interface, the token is stored in an `access_token` cookie after login, and each protected page checks it server-side before rendering.
Each protected endpoint decodes the token to identify the user and, where relevant, checks their role.
Frontend
In addition to the REST API, the project includes a server-rendered frontend built with Jinja2 templates, Bootstrap for styling, and vanilla JavaScript for handling form submissions and API calls from the browser.
Pages
Route	Description
`/todos/todo-page`	Displays the logged-in user's to-do items in a table, separating completed and incomplete items
`/todos/add-todo-page`	Form for creating a new to-do item
`/todos/edit-todo-page/{todo_id}`	Form for editing an existing to-do item, pre-filled with its current data
`/auth/login-page`	Login form
`/auth/register-page`	Registration form
Page routes check for a valid JWT stored in an `access_token` cookie. If the token is missing or invalid, the user is redirected to the login page.
Templates share a common `layout.html`, included at the top of each page, for consistent structure and styling across the site.
Database Migrations
Schema changes are managed with Alembic. To create a new migration after modifying `models.py`:
```
alembic revision -m "description of the change"
```
To apply migrations:
```
alembic upgrade head
```
Testing
The project includes automated tests written with pytest, covering authentication, CRUD operations on to-do items, and user profile updates. Tests run against a separate PostgreSQL test database, kept isolated from the main application database.
Database connection strings are loaded from environment variables using `python-dotenv`, so credentials are never hardcoded or committed to the repository.
To run the tests:
```
pytest
```
What's covered
Reading all to-do items for an authenticated user
Reading a single to-do item by id
Creating a new to-do item
Updating a user's phone number
Test data (users and to-do items) is created and cleaned up using pytest fixtures, ensuring each test run starts from a consistent state and does not leave leftover data in the test database.
Notes
This project was built as a learning exercise, with a focus on understanding how the different parts of a full-stack FastAPI application fit together: routers, dependencies, database sessions, request/response models, authentication, migrations, server-rendered templates, and testing.