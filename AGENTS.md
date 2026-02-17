# AGENTS.md - Developer Guidelines for Invoice Act Tracker

## Core Principles

- Write reasoning in English
- Always check the application for errors after making changes
- Use ports from 10000-10999 range for test runs
- Stop launched ports after checks (except port 8000 - user run)
- Use ruff linter for Python
- Follow best practices, avoid hacks
- If you need to stop user run (port 8000), stop it, but after all work notify that user run is stopped. User will restart it manually.

---

## Project

FastAPI web application for tracking invoices (from 1C) and signed acts (from SBIS), matching them, payment control, and KPI monitoring of responsible employees.

- **Language**: Python 3.10+
- **Framework**: FastAPI
- **Database**: SQLite with SQLAlchemy ORM
- **Package Manager**: uv
- **Dependencies**: See `pyproject.toml`

---

## Build, Run & Development Commands

### Running the Application

```bash
# Using the provided batch script (port 8000)
3_run.bat

# Or manually with uv (port 8000 - for user)
uv run uvicorn src.main:app --host 127.0.0.1 --port 8000 --reload

# For testing - use ports from 10000-10999 range
uv run uvicorn src.main:app --host 127.0.0.1 --port 10000 --reload
```

**Important:**
- Port 8000 is user run - do not stop it unless necessary
- Use ports 10000-10999 for test runs
- After checks, stop launched test ports

### Dependency Management

```bash
# Add a new dependency (automatically updates pyproject.toml)
uv add <package_name>

# Add a dev dependency
uv add --dev <package_name>
```

### Database Management

```bash
# Clear database (creates backup first)
clear_database.bat
# Or: python clear_database.py

# Restore from backup
restore_database.bat
# Or: python restore_database.py
```

### Linting & Type Checking

```bash
# Install ruff linter
uv add --dev ruff

# Run linter
uv run ruff check src/

# Run linter with auto-fix
uv run ruff check src/ --fix

# Format code
uv run ruff format src/
```

### Testing

```bash
# Run all tests
uv run pytest

# Run a single test file
uv run pytest tests/test_file.py

# Run a single test function
uv run pytest tests/test_file.py::test_function_name

# Run tests matching a pattern
uv run pytest -k "test_pattern"
```

---

## Code Style Guidelines

### Git Workflow

After making changes:
1. Run linter `uv run ruff check src/` and fix errors
2. Check application for errors
3. Create commit with message reflecting the essence of the change
4. Push changes to GitHub

```bash
# Commit example
git add .
git commit -m "Добавлена валидация email при импорте сотрудников"
git push
```

**Important:**
- Do not write generic commit messages like "Очередная итерация правок от пользователя"
- Commit message should reflect the specific change

### General Principles

- Follow PEP 8 style guide
- Use Python 3.10+ features (type hints, match/case where appropriate)
- Keep functions focused and small (< 50 lines when possible)
- Use meaningful variable and function names

### Best Practices

**Python:**
- Use ruff linter: `uv run ruff check src/`
- Fix all linter errors before commit
- Avoid bare except blocks
- Always close DB sessions in finally block

**JavaScript:**
- Use modern ES6+ syntax
- Avoid var, use const/let
- Follow consistent code style

### Imports

Order imports in each file:

1. Standard library (`os`, `re`, `datetime`, etc.)
2. Third-party packages (`fastapi`, `sqlalchemy`, `openpyxl`, etc.)
3. Local application imports (`from .database import ...`)

```python
# Example import order
import os
import re
from datetime import datetime, date, timedelta
from typing import Optional, List, Dict, Any
from functools import lru_cache

from fastapi import FastAPI, Request, Form, UploadFile, File
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from openpyxl import load_workbook

from .database import get_session, init_db, Contractor, Employee
```

### Type Hints

Always use type hints for function parameters and return types:

```python
# Good
def get_or_create_contractor(session, name: str, inn: str = None) -> Contractor:
    ...

def parse_datetime(value) -> Optional[datetime]:
    ...

# Avoid
def get_or_create_contractor(session, name, inn=None):
    ...
```

### Naming Conventions

- **Variables/functions**: snake_case (`get_session`, `invoice_amount`)
- **Classes**: PascalCase (`Contractor`, `Invoice`, `Employee`)
- **Constants**: UPPER_SNAKE_CASE (`MAX_FILE_SIZE`, `ALLOWED_EXTENSIONS`)
- **Private functions**: prefix with underscore (`_internal_helper`)

### Database Models (SQLAlchemy)

Follow this pattern:

```python
class Contractor(Base):
    __tablename__ = "contractors"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now)
    name = Column(Text, unique=True)
    inn = Column(Text)

    invoices = relationship("Invoice", back_populates="contractor")
```

### Error Handling

- Avoid bare `except:` clauses - catch specific exceptions
- Use try/except with proper logging or user feedback
- Return appropriate HTTP status codes in FastAPI endpoints

```python
# Good
try:
    result = risky_operation()
except ValueError as e:
    raise HTTPException(status_code=400, detail=str(e))

# Avoid
try:
    result = risky_operation()
except:
    pass  # Silent failure
```

### FastAPI Endpoints

```python
@app.get("/endpoint", response_class=HTMLResponse)
def endpoint_name(request: Request):
    session = get_session()
    try:
        # business logic
        return templates.TemplateResponse("template.html", {...})
    finally:
        session.close()
```

### HTML Templates

- Templates are in `src/templates/`
- Use Jinja2 syntax
- Helper functions like `format_contractor_name` are registered globally

### File Structure

```
src/
├── __init__.py
├── database.py      # SQLAlchemy models and DB utilities
├── main.py          # FastAPI app and routes
└── templates/       # HTML Jinja2 templates
    ├── dashboard.html
    ├── import.html
    └── ...
```

---

## Database Schema

| Table | Description |
|-------|-------------|
| contractors | Counterparties (normalized names) |
| employees | Employees (last_name, first_name, middle_name, department) |
| stop_words | Words used to filter imports |
| invoices | Invoices from 1C |
| acts | Acts from SBIS |

---

## Key Business Logic

### Contractor Normalization
- Removes punctuation, moves legal forms (OOO, IP, etc.) to end
- Example: TekhnoDrayv STROY OOO

### Invoice Filtering (1C Import)
1. Skip if amount == 0 or empty
2. Skip if comment contains "udalit" or "zagluшка"
3. Keep if responsible in RPO department OR surname in comment
4. Skip if comment contains stop words

### Act Filtering (SBIS Import)
1. Skip if document type == EDOSch
2. Keep if package type == DocOtpGrIskh (regardless of doc type)
3. Status must be "Execution completed successfully"
4. Signing date must be present

### Invoice Status Calculation
- **Not paid**: acts sum = 0 or no acts linked
- **Partially paid**: acts sum < invoice amount
- **Paid**: acts sum == invoice amount
- **Amount error**: acts sum > invoice amount (requires attention)

---

## Common Tasks

### Adding a New Endpoint

1. Add route in `src/main.py`:
```python
@app.get("/new-page", response_class=HTMLResponse)
def new_page(request: Request):
    return templates.TemplateResponse("new_page.html", {"request": request})
```

2. Create template in `src/templates/new_page.html`

### Adding a New Database Model

1. Add class in `src/database.py`
2. Import and use in `src/main.py`:
```python
from .database import NewModel, get_session

@app.post("/create")
def create_item():
    session = get_session()
    try:
        item = NewModel(...)
        session.add(item)
        session.commit()
        return {"id": item.id}
    finally:
        session.close()
```

---

## Testing Guidelines

When adding tests:

```python
# tests/test_database.py
import pytest
from src.database import get_session, Contractor

def test_contractor_creation():
    session = get_session()
    try:
        contractor = Contractor(name="Test Company")
        session.add(contractor)
        session.commit()
        assert contractor.id is not None
    finally:
        session.rollback()
        session.close()
```

Use fixtures in `conftest.py` for shared setup.
