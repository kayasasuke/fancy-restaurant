# reservation-form-input Specification

## Purpose
TBD - created by archiving change ex8-reservation-form. Update Purpose after archive.
## Requirements
### Requirement: Visitors can submit reservation input
The system SHALL provide a Django reservation form with customer name, guest count, reservation date, and a time-slot choice populated from persisted time slots.

#### Scenario: Visitor opens the reservation form
- **WHEN** a visitor sends a GET request to `/reservations/new/`
- **THEN** the system renders an empty form with the available time slots

#### Scenario: Visitor submits invalid input
- **WHEN** a visitor sends a POST request with missing, invalid, or unavailable form values
- **THEN** the system re-renders the form with validation errors and creates no customer or reservation

### Requirement: Valid guest input creates a reservation
The system SHALL create a guest customer and reservation after a valid form submission, assigning the smallest suitable unoccupied existing table for the requested date and time slot.

#### Scenario: Visitor submits a valid reservation
- **WHEN** a visitor submits a valid name, guest count, date, and available time slot with a suitable table
- **THEN** the system creates the customer and reservation, then redirects to that reservation's detail URL

#### Scenario: No suitable table is available
- **WHEN** a visitor submits otherwise valid input but no existing table can accommodate the party for the requested date and time slot
- **THEN** the system re-renders the form with a form-level availability error and creates no customer or reservation
