# PathPilot AI — Backend

FastAPI backend for the PathPilot AI personalized learning-path generator.

## Tech Stack

| Layer       | Technology            |
| ----------- | --------------------- |
| Framework   | FastAPI               |
| ORM         | SQLAlchemy            |
| DB Driver   | PyMySQL               |
| Validation  | Pydantic              |
| Config      | python-dotenv         |
| Server      | Uvicorn               |

## Project Structure

```
backend/
├── app/
│   ├── __init__.py        # App package
│   ├── main.py            # FastAPI entry-point
│   ├── core/              # Config, security, constants
│   ├── database/          # Engine, session, Base
│   ├── models/            # SQLAlchemy ORM models
│   ├── schemas/           # Pydantic request/response schemas
│   ├── routers/           # API route modules
│   ├── services/          # Business-logic layer
│   ├── ai/                # LLM integrations
│   └── utils/             # Shared helpers
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Quick Start

```bash
# 1 — Create & activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

# 2 — Install dependencies
pip install -r requirements.txt

# 3 — Copy env file and edit values
cp .env.example .env

# 4 — Run the dev server
uvicorn app.main:app --reload --port 8000
```

## API Docs

- **Swagger UI** → [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**      → [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Health Check

```
GET http://localhost:8000/api/health
```

Response:

```json
{
  "status": "ok",
  "message": "PathPilot AI backend is running"
}
```
