# Inventory Stack (React + FastAPI + PostgreSQL)

Minimal implementation for the technical test.

## Features

- **Front-end (React + Vite)**: List stock (SKU, EAN13, quantity), update quantity, view movement history.
- **Back-end (FastAPI)**: Items API, update quantity endpoint (+movement log), movement history endpoint.
- **DB (PostgreSQL)** via SQLAlchemy.
- **Bonus**: JWT auth (`/auth/token`) – required for quantity updates. Demo user seeded `admin/admin123`.
- **Bonus**: Basic tests (pytest + vitest).

## Run with Docker (recommended)

```bash
docker compose up --build
```

Then:
- API: http://localhost:8000/docs
- Front: http://localhost:5173
- Login with `admin / admin123` (seeded).

## Run locally (no Docker)

**Backend**
```bash
cd backend
python -m venv .venv && . .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # adjust DATABASE_URL if needed
# Make sure Postgres is running and u have created a database (default: postgres/postgres on localhost:5432, db=inventory)
python seed.py
uvicorn app.main:app --reload
```

**Frontend**
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

## API Summary

- `GET /items` → List items
- `PATCH /items/{item_id}/quantity` (JWT) → `{ quantity, reason? }`
- `GET /movements?limit=50` → Most recent movements
- `POST /auth/token` (form-data) → `{ access_token }` (demo user seeded)

## Tests

**Backend**
```bash
cd backend
pytest -q
```

**Frontend**
```bash
cd frontend
npm run test
```

## Notes

- EAN13 is validated as 13 digits. You can extend with checksum if required.
- Movements log records *delta* when quantity changes (positive for entries, negative for exits).
- CORS is enabled for Vite dev server.
```
