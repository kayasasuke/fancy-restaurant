## MODIFIED Requirements

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
The system SHALL expose a template-rendered URL representing the future reservation form page.

#### Scenario: Visitor opens reservation form placeholder
- **WHEN** a visitor requests `/reservations/new/`
- **THEN** the system returns a successful template-rendered response showing the currently hard-coded sample reservation values

### Requirement: Reservation detail is callable
The system SHALL expose a template-rendered URL that shows one reservation by ID.

#### Scenario: Visitor opens existing reservation detail
- **WHEN** a visitor requests `/reservations/<id>/` for an existing reservation
- **THEN** the system returns a successful template-rendered response containing the reservation details

#### Scenario: Visitor opens missing reservation detail
- **WHEN** a visitor requests `/reservations/<id>/` for a missing reservation
- **THEN** the system returns a 404 response
