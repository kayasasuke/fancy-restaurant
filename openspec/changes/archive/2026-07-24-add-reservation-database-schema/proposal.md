## Why

Exercise 5 requires the project to move from a runnable Django scaffold to a runnable Django application with an initial database schema. The reservation domain needs persistent tables for restaurant tables, reservation time slots, and reservations before booking behavior can be implemented.

## What Changes

- Add reservation-domain models in `reservations/models.py`.
- Provide readable `__str__()` labels for Django admin and shell use.
- Register the new models in `reservations/admin.py`.
- Generate and apply the initial reservation migration.
- Add focused model tests for string labels, table ordering, and reservation uniqueness.
- Update project documentation and OpenSpec requirements to describe the database design.

## Capabilities

### New Capabilities

- `reservation-database-schema`: Defines the initial Django ORM schema for tables, time slots, and reservations.

### Modified Capabilities

- None.

## Impact

- Affects `reservations/models.py`, `reservations/admin.py`, reservation migrations, tests, README documentation, and OpenSpec specs.
- Uses the existing SQLite database configuration and existing registered `reservations` Django app.
- Does not add external dependencies or user-facing reservation views.
