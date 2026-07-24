## MODIFIED Requirements

### Requirement: Sample reservation creation redirects
The system SHALL expose a URL that creates a simple sample reservation on POST and redirects to its detail page when a suitable table exists. It MUST NOT create new restaurant tables as part of this action.

#### Scenario: Visitor creates sample reservation
- **WHEN** a visitor sends a POST request to `/reservations/sample-create/` and a suitable table is available
- **THEN** the system creates a reservation with hard-coded sample values and redirects to `/reservations/<id>/`

#### Scenario: Visitor opens sample creation URL with GET
- **WHEN** a visitor sends a GET request to `/reservations/sample-create/`
- **THEN** the system returns a 405 response and does not create a reservation

#### Scenario: No suitable table is available
- **WHEN** a visitor sends a POST request to `/reservations/sample-create/` and no table can accommodate the sample party
- **THEN** the system returns `409 Conflict` and creates neither a table nor a reservation
