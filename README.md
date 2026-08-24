# FarmEra Backend

Backend service for **FarmEra**, an online farming game. The project provides player authentication, player data management and inventory functionality through a REST API.

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- JWT authentication
- Google OAuth 2.0
- Uvicorn

## Features

- Google ID token authentication
- Google Authorization Code + PKCE login flow
- JWT-based player sessions
- Automatic player creation on first login
- Player profile endpoint
- Player inventory system
- Starter item granting
- PostgreSQL persistence
- Alembic database migrations
- Health and database connectivity endpoints

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/auth/google` | Login with a Google ID token |
| `POST` | `/auth/google/code` | Login using Google Authorization Code + PKCE |
| `GET` | `/players/me` | Return the authenticated player |
| `GET` | `/inventory/me` | Return the authenticated player's inventory |
| `GET` | `/health` | API health check |
| `GET` | `/db-health` | Database connectivity check |

Protected endpoints require a bearer token:

```http
Authorization: Bearer <access_token>
```

## Project Structure

```text
app/
├── api/          # API routes and dependencies
├── core/         # Configuration and security
├── db/           # Database session and base configuration
├── models/       # SQLAlchemy models
├── schemas/      # Pydantic request/response schemas
├── services/     # Authentication and inventory services
└── main.py       # FastAPI application

migrations/       # Alembic migrations
```

## Installation

Clone the repository:

```bash
git clone https://github.com/g0khanbey/farmera-backend.git
cd farmera-backend
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+psycopg://username:password@localhost:5432/farmera
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
JWT_SECRET=your_secure_random_secret
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

The `.env` file is ignored by Git and should never be committed.

## Database Migrations

Apply all migrations:

```bash
alembic upgrade head
```

Create a new migration after changing database models:

```bash
alembic revision --autogenerate -m "migration description"
```

## Running the API

Development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI interactive documentation:

```text
http://127.0.0.1:8000/docs
```

## Authentication Flow

1. The client authenticates with Google.
2. FarmEra verifies the Google ID token or exchanges the authorization code.
3. A new player is created automatically when the Google identity is seen for the first time.
4. The backend returns a signed JWT access token.
5. The client sends that token as a bearer token when accessing protected endpoints.

## Current Status

The project is under active development. Current backend functionality focuses on authentication, player data and the inventory foundation for future gameplay systems.
