## MODIFIED Requirements

### Requirement: Reservation form placeholder is callable
The system SHALL expose a template-rendered reservation form at `/reservations/new/` that accepts GET to display the form and POST to process visitor input.

#### Scenario: Visitor opens reservation form placeholder
- **WHEN** a visitor sends a GET request to `/reservations/new/`
- **THEN** the system returns a successful template-rendered response with the reservation input form

#### Scenario: Visitor submits reservation form
- **WHEN** a visitor sends a POST request to `/reservations/new/`
- **THEN** the system validates the submitted reservation input and either redirects to the created reservation or re-renders the form with errors

## REMOVED Requirements

### Requirement: Sample reservation creation redirects
**Reason**: Exercise 8 replaces the hard-coded sample booking with visitor-supplied reservation input.
**Migration**: Submit reservation input to `/reservations/new/` with POST instead.
