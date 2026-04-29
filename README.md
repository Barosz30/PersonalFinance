# Personal Finance API

FastAPI project for learning Python backend best practices: typing, validation, auth,
database migrations, tests, and clean architecture.

## Run locally

1. Create and activate a virtual environment.
2. Install dependencies:
   - `pip install -e .[dev]`
3. Copy `.env.example` to `.env` and edit values.
4. Start API:
   - `uvicorn app.main:app --reload`

## Migrations

- Initialize DB schema:
  - `alembic upgrade head`

## Test and quality

- `pytest`
- `ruff check .`
- `black --check .`
- `mypy app`
