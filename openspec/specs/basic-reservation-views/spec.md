## Purpose
Define the first callable Django URLs and simple function-based views for the reservation app.

## Requirements

### Requirement: Home page is callable
The system SHALL expose a home page URL for the reservation app.

#### Scenario: Visitor opens home page
- **WHEN** a visitor requests `/`
- **THEN** the system returns a successful response describing the reservation app and links to basic actions

### Requirement: Table list is callable
The system SHALL expose a URL that lists active restaurant tables.

#### Scenario: Visitor opens table list
- **WHEN** a visitor requests `/tables/`
- **THEN** the system returns a successful response containing active table records ordered by capacity and table number

### Requirement: Time slot list is callable
The system SHALL expose a URL that lists active reservation time slots.

#### Scenario: Visitor opens time slot list
- **WHEN** a visitor requests `/time-slots/`
- **THEN** the system returns a successful response containing active time slot records ordered by start time

### Requirement: Reservation form placeholder is callable
The system SHALL expose a URL representing the future reservation form page.

#### Scenario: Visitor opens reservation form placeholder
- **WHEN** a visitor requests `/reservations/new/`
- **THEN** the system returns a successful response showing the currently hard-coded sample reservation values

### Requirement: Sample reservation creation redirects
The system SHALL expose a URL that creates a simple sample reservation on POST and redirects to its detail page.

#### Scenario: Visitor creates sample reservation
- **WHEN** a visitor sends a POST request to `/reservations/sample-create/`
- **THEN** the system creates a reservation with hard-coded sample values and redirects to `/reservations/<id>/`

#### Scenario: Visitor opens sample creation URL with GET
- **WHEN** a visitor sends a GET request to `/reservations/sample-create/`
- **THEN** the system returns a 405 response and does not create a reservation

### Requirement: Reservation detail is callable
The system SHALL expose a URL that shows one reservation by ID.

#### Scenario: Visitor opens existing reservation detail
- **WHEN** a visitor requests `/reservations/<id>/` for an existing reservation
- **THEN** the system returns a successful response containing the reservation details

#### Scenario: Visitor opens missing reservation detail
- **WHEN** a visitor requests `/reservations/<id>/` for a missing reservation
- **THEN** the system returns a 404 response
