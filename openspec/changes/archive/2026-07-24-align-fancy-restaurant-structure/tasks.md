## 1. Project and App Structure

- [x] 1.1 Rename the Django project package to `FancyRestaurant` and update management, ASGI, WSGI, pytest, and OpenSpec references.
- [x] 1.2 Rename the Django app package to `FancyRestaurantApp`, update imports, and preserve the `reservations` Django app label.
- [x] 1.3 Verify the existing migration history is recognized and apply the compatible schema migration.

## 2. Domain Integrity and Tests

- [x] 2.1 Change sample reservation creation so it never creates restaurant tables when capacity is unavailable.
- [x] 2.2 Add tests for no-table availability and preserved table inventory.

## 3. Documentation and Tooling

- [x] 3.1 Update README with the architecture sketch, customer schema explanation, and complete URL API request parameters.
- [x] 3.2 Update AGENTS.md to reflect the completed application structure and current tooling.
- [x] 3.3 Configure Black for Python 3.10 and Pylint for Django.

## 4. Schema Simplification

- [x] 4.1 Replace the extended Exercise 5 models with `Customer`, `Table`, `TimeSlot`, and `Reservation` fields that match the instructor's introductory schema style.
- [x] 4.2 Add a forward data migration that creates a `Customer` for each existing reservation before removing obsolete fields.
- [x] 4.3 Update admin registration, sample views, model tests, README, and agent guidance for the simplified schema.

## 5. Verification

- [x] 5.1 Run Django system checks, migration checks, pytest, Black, Pylint, and OpenSpec validation.
