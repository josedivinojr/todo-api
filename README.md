# 📝 ToDo API

A ToDo API built with **FastAPI**, **Pydantic**, **SQLAlchemy**, and **Poetry**.
It offers full user and task management, token-based authentication, and a flexible development experience using Docker.

## 🚀 Features

### 🤺 User Management
- Create new users
- List users with pagination
- Retrieve specific user details
- Update user information
- Delete users

### 🔐 Authentication
- Login to receive an access token
- Refresh tokens for continued access

### ✅ ToDo Task Management
- Create new to-do tasks
- List tasks for authenticated users with filtering (title, description, status) and pagination
- Update task details
- Delete tasks

## ⚙️ Tech Stack

- **FastAPI** – Web framework for fast APIs
- **Pydantic** – Data validation using Python type hints
- **SQLAlchemy** – ORM for database operations
- **Poetry** – Python dependency management
- **Alembic** – Database migrations
- **PostgreSQL** – Production-ready relational database
- **SQLite** – Lightweight DB for local dev (default fallback)
- **Docker & Docker Compose** – Containerization
- **PyJWT** – JWT token generation & validation
- **passlib** – Password hashing

## 🛠️ Setup & Installation

### 🔧 Prerequisites

- Python 3.8+
- [Poetry](https://python-poetry.org/docs/#installation)
- Docker & Docker Compose

### 🐳 Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/josedivinojr/todo-api
   cd todo-api
   ```

2. **Configure environment**
   ```bash
   cp .env_example .env
   # Customize your SECRET_KEY and other variables
   ```

3. **Start services**
   ```bash
   docker-compose up --build
   ```

4. **Run migrations in container**
   ```bash
   docker-compose exec todo_app poetry run alembic upgrade head
   ```

5. **Stop everything**
   ```bash
   docker-compose down
   ```

## 📡 API Reference

All endpoints are prefixed with `/v1`.

### 🧑 Users (`/v1/users`)
| Method | Endpoint         | Description                          |
|--------|------------------|--------------------------------------|
| POST   | `/`              | Create a new user                    |
| GET    | `/`              | List users (auth required)          |
| GET    | `/{user_id}`     | Get user by ID (auth required)      |
| PUT    | `/{user_id}`     | Update user (auth + ownership)      |
| DELETE | `/{user_id}`     | Delete user (auth + ownership)      |

### 🔑 Auth (`/v1/auth`)
| Method | Endpoint             | Description                      |
|--------|----------------------|----------------------------------|
| POST   | `/token`             | Login (OAuth2PasswordRequestForm)|
| POST   | `/refresh_token`     | Refresh access token             |

### ✅ ToDos (`/v1/todos`)
| Method | Endpoint         | Description                         |
|--------|------------------|-------------------------------------|
| POST   | `/`              | Create new task (auth required)     |
| GET    | `/`              | List tasks (filtering + pagination) |
| PATCH  | `/{todo_id}`     | Update task (auth + ownership)      |
| DELETE | `/{todo_id}`     | Delete task (auth + ownership)      |

## 🧪 Running Tests

```bash
poetry run pytest tests
```
