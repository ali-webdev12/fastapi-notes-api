# FastAPI Notes API

A backend notes API built with FastAPI, Python, JWT, and SQLite. It provides user authentication and full note management while ensuring each user can only access and modify their own notes.

## Features

- User registration and login
- Secure password hashing
- JWT token-based authentication
- SQLite relational database (`users` and `notes` tables with foreign key constraints and cascade deletion)
- Full CRUD operations for notes with strict user ownership verification

## Project Structure

```text
fastapi-notes-api/
├── main.py            # FastAPI application entry point and router setup
├── auth.py            # Authentication routes, password hashing, and JWT logic
├── notes.py           # Protected notes CRUD routes
├── database.py        # SQLite connection and database operations
├── requirements.txt   # Project dependencies
└── .gitignore         # Ignored files (.env, database, virtual environment)
```

## Getting Started

### 1. Clone the repository
```bash
git clone [https://github.com/ali-webdev12/fastapi-notes-api.git](https://github.com/ali-webdev12/fastapi-notes-api.git)
cd fastapi-notes-api
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a `.env` file in the root directory and add your secret key:
```env
KEY_SECURITY=your_secret_key_here
```

### 5. Run the local server
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 3000
```

The API will be available at `http://127.0.0.1:3000`, and interactive API docs (Swagger UI) can be accessed at `http://127.0.0.1:3000/docs`.

## API Endpoints

### Authentication
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/register` | Create a new user account with `username` and `password` | No |
| `POST` | `/login` | Authenticate user credentials and return a JWT token | No |
| `DELETE` | `/delete` | Delete the current user account and all associated notes | Yes (Bearer Token) |

### Notes
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/notes/create` | Create a new note for the authenticated user | Yes (Bearer Token) |
| `GET` | `/notes/get_all` | Retrieve all notes belonging to the authenticated user | Yes (Bearer Token) |
| `PATCH` | `/notes/edit` | Update the `content` of a specific note owned by the user | Yes (Bearer Token) |
| `DELETE` | `/notes/delete` | Delete a specific note owned by the user | Yes (Bearer Token) |

## Authentication Usage

For protected routes, include the JWT token in the `Authorization` header:

```http
Authorization: Bearer <your_access_token>
```
