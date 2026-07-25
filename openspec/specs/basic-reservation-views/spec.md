## Purpose
Define the first callable Django URLs and simple function-based views for the reservation app.
## Requirements
### Requirement: Home page is callable
The system SHALL expose a home page URL for the reservation app and render it through a Django template.

#### Scenario: Visitor opens home page
- **WHEN** a visitor requests `/`
- **THEN** the system returns a successful template-rendered response describing the reservation app and linking to basic actions

### Requirement: Table list is callable
The system SHALL expose a template-rendered URL that lists restaurant tables.

#### Scenario: Visitor opens table list
- **WHEN** a visitor requests `/tables/`
- **THEN** the system returns a successful template-rendered response containing table records ordered by capacity and table number

### Requirement: Time slot list is callable
The system SHALL expose a template-rendered URL that lists reservation time slots.

#### Scenario: Visitor opens time slot list
- **WHEN** a visitor requests `/time-slots/`
- **THEN** the system returns a successful template-rendered response containing time slot records ordered by start time

### Requirement: Reservation form placeholder is callable
The system SHALL expose a template-rendered reservation form at `/reservations/new/` that accepts GET to display the form and POST to process visitor input.

#### Scenario: Visitor opens reservation form placeholder
- **WHEN** a visitor sends a GET request to `/reservations/new/`
- **THEN** the system returns a successful template-rendered response with the reservation input form

#### Scenario: Visitor submits reservation form
- **WHEN** a visitor sends a POST request to `/reservations/new/`
- **THEN** the system validates the submitted reservation input and either redirects to the created reservation or re-renders the form with errors

### Requirement: Reservation detail is callable
The system SHALL expose a template-rendered URL that shows one reservation by ID.

#### Scenario: Visitor opens existing reservation detail
- **WHEN** a visitor requests `/reservations/<id>/` for an existing reservation
- **THEN** the system returns a successful template-rendered response containing the reservation details

#### Scenario: Visitor opens missing reservation detail
- **WHEN** a visitor requests `/reservations/<id>/` for a missing reservation
- **THEN** the system returns a 404 response
