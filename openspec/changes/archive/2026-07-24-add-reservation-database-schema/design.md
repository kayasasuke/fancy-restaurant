## Context

The project already contains a runnable Django project package named `config` and a registered app named `reservations`. The app currently has empty model and admin files, so the database does not yet represent the restaurant reservation domain described in the README.

Exercise 5 focuses on creating the application database through Django models, migrations, admin registration, and readable object labels.

## Goals / Non-Goals

**Goals:**

- Define the initial reservation database schema using Django ORM models.
- Support restaurant tables, reusable time slots, and dated reservations.
- Allow reservations to belong to either a logged-in Django user or a typed customer name.
- Add database constraints that prevent double-booking the same table for the same date and time slot.
- Keep the schema simple enough for the current exercise while leaving room for later table-assignment logic.

**Non-Goals:**

- Implement booking views, forms, authentication screens, or suggestion algorithms.
- Replace Django's built-in user model.
- Add external database engines or non-Django dependencies.

## Decisions

- Use Django's built-in `auth.User` instead of a custom user model.
  - Rationale: the README allows login or typed name, and the current project has not introduced a custom auth model.
  - Alternative considered: custom `User` model. That would add migration complexity too early.

- Model reservation times with a `TimeSlot` table instead of storing raw times only on reservations.
  - Rationale: this supports an admin-managed list of available booking times and later nearby-slot suggestions.
  - Alternative considered: `TimeField` directly on `Reservation`. This is simpler but weaker for admin management and future availability queries.

- Store both `reservation_date` and `time_slot` on `Reservation`.
  - Rationale: slots are reusable across dates, while reservations are date-specific.
  - Alternative considered: a dated slot table. That can be introduced later if the app needs per-date slot capacity or closures.

- Add unique constraints for table identity, slot time, and table/date/slot reservations.
  - Rationale: the database should protect core invariants even before full booking services exist.
  - Alternative considered: enforcing all conflicts in Python only. That risks accidental duplicate records from admin or scripts.

## Risks / Trade-offs

- The schema does not yet assign the smallest available table automatically -> later service logic must query `Table` ordered by capacity.
- A single `TimeSlot` duration applies globally -> future features may need per-slot or per-reservation durations.
- Guest count is stored on the reservation, not derived from related guests -> this matches the current app scope and keeps Exercise 5 focused.

## Migration Plan

1. Add models and admin registrations.
2. Run `makemigrations reservations`.
3. Run `migrate` to create the SQLite database tables.
4. Add and run model tests plus Django system checks.

Rollback is the standard Django migration rollback for the generated reservation migration.
