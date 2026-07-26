## Why

The reservation form uses persisted table and time-slot choices, but a new local database contains neither. Visitors therefore cannot select a time slot or create a reservation.

## What Changes

- Add a Django fixture with a small set of restaurant tables and evening time slots.
- Document the fixture loading command.
- Test that the fixture supplies usable table and time-slot data.

## Out Of Scope

- Table-management screens, seed customers, reservations, or schema changes.
