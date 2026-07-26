## Context

`ReservationForm` obtains its time-slot choices from the database and table selection requires persisted tables. A fixture is the smallest reproducible way to prepare an otherwise empty local database without adding an administration workflow.

## Decisions

- Store `initial_restaurant_data.json` in the app's standard `fixtures` directory.
- Use the stable `reservations` app label in fixture model identifiers.
- Seed four tables for parties of two, four, and six and three evening time slots.
- Do not add customers or reservations, so each loaded time slot begins available.

## Non-Goals

- Do not introduce a data migration, admin interface, management command, or table/time-slot CRUD screen.
