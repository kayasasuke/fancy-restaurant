## Why

The current project is functionally runnable, but its Django package names and several project documents no longer align with the Fancy Restaurant theme, the completed Exercise 1-6 work, or the instructor's reference project structure. The sample reservation action also creates new restaurant tables when none are available, which conflicts with the fixed-table restaurant domain.

## What Changes

- **BREAKING** Rename the Django project package from `config` to `FancyRestaurant` and the reservation app package from `reservations` to `FancyRestaurantApp`, following the instructor's project/app naming pattern.
- Preserve the existing Django migration label and database table identity as `reservations` so existing local SQLite databases remain compatible.
- Prevent the sample reservation action from creating new tables; it will report that the sample cannot be created when no suitable table is available.
- Simplify the reservation schema to the Exercise 5 scope and represent a restaurant user with a `Customer` model, following the instructor's `Patient` model pattern.
- Bring the README, AGENTS.md, URL API documentation, and lint configuration in line with the completed exercises.

## Capabilities

### New Capabilities
- `fancy-restaurant-project-structure`: Define the canonical Django project/app package structure and compatibility rules for the Fancy Restaurant application.

### Modified Capabilities
- `basic-reservation-views`: The sample reservation action must preserve the fixed restaurant table inventory when no suitable table is available.
- `agentic-project-setup`: Agent-facing guidance must name the current Django project and app packages.
- `reservation-database-schema`: Reduce the schema to the basic customer, table, time slot, and reservation records required at this course stage.

## Impact

- Renames the Django project and app packages and updates Python imports, settings references, migrations package locations, and test configuration.
- Updates the sample reservation response for the no-availability case and adds focused tests.
- Adds `pylint-django` configuration and a Python 3.10 Black target.
- Updates project and agent documentation; no remote changes or generated database files are included.
