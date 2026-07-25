## ADDED Requirements

### Requirement: Reservation form can check availability dynamically
The system SHALL let a visitor check the availability of a proposed party size, date, and time slot without reloading the reservation page.

#### Scenario: Visitor changes complete availability input
- **WHEN** a visitor changes the guest count, reservation date, or time slot after providing valid reservation input
- **THEN** the browser sends an HTMX request and replaces only the availability-result region with a server-rendered fragment

#### Scenario: Suitable table is available
- **WHEN** the availability request specifies a date, time slot, and guest count that an existing unoccupied table can accommodate
- **THEN** the response identifies the smallest suitable table and creates no customer or reservation

#### Scenario: No suitable table is available
- **WHEN** the availability request specifies otherwise valid input but no existing table can accommodate the party
- **THEN** the response reports that no suitable table is available and creates no customer or reservation

#### Scenario: Availability input is incomplete or invalid
- **WHEN** the availability request lacks a valid guest count, date, or known time slot
- **THEN** the response is an empty availability fragment and creates no customer or reservation

### Requirement: Ordinary reservation submission remains available
The system SHALL preserve the existing full-page reservation POST workflow while adding the dynamic availability query.

#### Scenario: Visitor submits a reservation
- **WHEN** a visitor submits the reservation form normally
- **THEN** the system uses the existing reservation creation behavior and redirects to the reservation detail on success
