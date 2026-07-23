# Agent Instructions

## Project Overview

Fancy Restaurant Reservation System is a Django web application for restaurant table reservations. Users should be able to log in or enter their name, choose a guest count, date, and time slot, then confirm a booking. The system should assign the smallest available table that fits the party size. If no table is available for the requested slot, it should suggest a nearby time slot or date.

Planned domain entities from the README are:

- User
- Table
- Reservation
- Time Slot

## Current Project Structure

- `README.md`: project outline, user flow, planned data model, and development environment notes.
- `pyproject.toml`: uv-managed Python project metadata and dependencies.
- `uv.lock`: locked dependency resolution.
- `.python-version`: Python `3.10.4`.
- `manage.py`: Django management command entrypoint.
- `config/`: Django project package.
- `config/settings.py`: default Django settings, currently using SQLite.
- `config/urls.py`: root URL configuration with the default admin route.
- `config/asgi.py`: ASGI application entrypoint.
- `config/wsgi.py`: WSGI application entrypoint.
- `main.py`: original scaffold entrypoint; not part of the Django runtime.
- `tests/test_sample.py`: current pytest smoke test.
- `pytest.ini`: pytest configuration file, currently empty.
- `.pylintrc`: pylint configuration file, currently empty.

No Django apps have been created yet.

## Setup and Commands

Use `uv` for dependency and command execution.

```bash
uv sync
uv run django-admin --version
uv run python manage.py check
uv run python manage.py runserver
uv run pytest
uv run coverage run -m pytest
uv run coverage report
```

When adding dependencies, use `uv add` so `pyproject.toml` and `uv.lock` stay in sync.

## Coding Conventions

- Follow the existing Python style: 4-space indentation, clear names, and simple functions.
- Keep formatting compatible with Black.
- Prefer small, focused Django apps once app creation begins.
- Keep models, forms, views, services, and tests organized by app.
- Put reservation rules, table assignment, availability checks, and suggestion logic outside views where practical. Views should coordinate HTTP input/output and call domain or service functions for business behavior.
- Add focused tests for reservation behavior as it is implemented, especially table selection and unavailable-slot suggestions.
- Do not commit generated files such as `__pycache__/`, `.pyc`, `.pytest_cache/`, coverage output, local SQLite databases, or virtual environments.

## Verification

Before handing off code changes, run:

```bash
uv run python manage.py check
uv run pytest
```

Use coverage commands when changing core reservation logic or shared behavior.

## Git Safety

- Do not overwrite unrelated user changes.
- Do not revert files unless explicitly requested.
- Do not commit generated files.
- Do not push to any remote unless explicitly requested.
- Check `git status --short --branch` before summarizing changes.
