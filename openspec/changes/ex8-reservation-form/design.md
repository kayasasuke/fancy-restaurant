## Context

Exercise 7 added templates but the reservation page still posts hard-coded values to a sample endpoint. The instructor's `ReserveForm` demonstrates a Django form with a name, database-derived choice, and date field, while its registration, login, and HTMX behavior belong to later work.

## Goals / Non-Goals

**Goals:**

- Replace the sample reservation action with one validated reservation form.
- Use Django form validation for the first visitor-supplied reservation values.
- Preserve the fixed restaurant table inventory and redirect to the existing detail page after a successful booking.

**Non-Goals:**

- Add account registration, login, password verification, or session authentication.
- Add HTMX validation, CSS, JavaScript, alternative-slot suggestions, cancellation, or concurrency controls.
- Change the database schema or add a migration.

## Decisions

- Define `ReservationForm` in `FancyRestaurantApp/forms.py` with `customer_name`, `guest_count`, `reservation_date`, and `time_slot` fields.
  - This follows the lecture's separate-form-module pattern and gives field-level validation before database writes.
  - The time-slot choices are supplied from `TimeSlot` records during form construction, following the instructor's dynamic choice pattern.

- Use `GET /reservations/new/` to render an empty form and `POST /reservations/new/` to process it.
  - GET is appropriate for retrieving the form; POST is appropriate because it creates persistent data.
  - A separate processing endpoint is unnecessary for this first form.

- On successful guest input, create a `Customer` with empty `login` and `password` values and select the smallest unoccupied existing table that fits the party.
  - This mirrors the instructor's guest-patient creation without prematurely adding an account workflow.
  - No suitable table is a form-level error and does not create a customer or reservation.

## Risks / Trade-offs

- [Concurrent requests can select the same table] -> This first form does not add transaction or locking behavior; concurrency handling remains later reservation logic.
- [Guest customers may repeat by name] -> The introductory guest workflow intentionally creates a customer record for each submitted reservation, matching the instructor's non-logged-in path.
- [No time slots exist] -> The form displays an empty choice list and rejects submitted values without database writes.

## Migration Plan

1. Add the form and update the reservation template and view.
2. Remove the hard-coded sample endpoint and its tests.
3. Add form and workflow tests, then run Django checks and pytest.
4. Roll back by restoring the sample endpoint; no data migration is required.
