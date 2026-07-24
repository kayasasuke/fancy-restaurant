## Context

The instructor's reference repository uses a project package named after the application and a separate app package with an `App` suffix. This project currently uses generic `config` and `reservations` packages. It also has completed Exercise 5 and 6 functionality that must keep working after a rename.

Existing migrations use the Django application label `reservations`, and local SQLite databases may have already applied those migrations. The domain has a fixed inventory of restaurant tables, so a customer-facing reservation action must never create additional tables to make a booking succeed.

## Goals / Non-Goals

**Goals:**

- Make the visible project and app package names match the Fancy Restaurant theme and the instructor's project/app structure.
- Preserve migration discovery and existing `reservations_*` database tables.
- Keep the successful sample-reservation redirect while preventing table inventory mutation when no table is available.
- Make completed-exercise documentation and local quality-tool configuration accurate.

**Non-Goals:**

- Build login or password-verification behavior for the new `Customer` model.
- Build login, session, template, form, availability-suggestion, or HTMX functionality.
- Rename existing database tables or rewrite applied migrations.

## Decisions

- Rename the project package to `FancyRestaurant` and the app package to `FancyRestaurantApp`.
  - This mirrors `Dentistry` and `DentistryApp` while retaining the Fancy Restaurant project name.
  - The generic `config`/`reservations` structure is valid Django, but does not communicate the course project's identity as clearly.

- Set `FancyRestaurantAppConfig.label = "reservations"`.
  - Django imports the new package via its `name`, while the stable label keeps the migration module, migration history, and default database table names compatible.
  - Changing the label would make Django treat the app as a new migration namespace and risk duplicate tables in existing databases.

- On no suitable table, the sample action returns `409 Conflict` and creates neither a table nor a reservation.
  - A `409` makes the capacity conflict explicit without claiming a successful booking.
  - Creating a new table is rejected because the theme defines a fixed restaurant inventory. Nearby-slot suggestions remain a later feature.

- Use a simple `Customer` model for restaurant users, mirroring the instructor's `Patient` model.
  - `Customer` owns `name`, `login`, and `password` fields, while `Reservation` always belongs to one customer.
  - This is domain data only; login and password verification are explicitly deferred to the later authentication exercise.

## Risks / Trade-offs

- [Case-sensitive package names] → Update every Python settings/import reference and verify with Django commands and pytest.
- [Existing local database] → Preserve the `reservations` app label and do not rewrite migrations or table names.
- [Sample action no longer self-seeds a table] → Update tests to create the required table explicitly; this reflects the fixed inventory requirement.
- [Pylint becomes stricter] → Add the Django plugin and targeted project configuration rather than suppressing ORM errors globally.

## Migration Plan

1. Move project and app packages, then update settings entry points and imports.
2. Keep the app label `reservations` and run `showmigrations` against the existing database configuration.
3. Update the sample reservation behavior and tests.
4. Run Django checks, migrations checks, pytest, Black, Pylint, and OpenSpec validation.
5. Back up the database, then apply the forward data migration. It creates a `Customer` for every existing reservation before obsolete fields are removed and stops if a legacy customer name exceeds the course-aligned 20-character limit.
6. Roll back package renames from Git before deployment, or restore the database from backup if the schema migration must be reversed.
