## ADDED Requirements

### Requirement: Customers are persisted
The system SHALL persist restaurant customers with a name, login, and password value.

#### Scenario: Admin views customer records
- **WHEN** a customer record is listed in Django admin or the Django shell
- **THEN** the object label includes the customer name

## MODIFIED Requirements

### Requirement: Restaurant tables are persisted
The system SHALL persist restaurant tables with a table number and seating capacity.

#### Scenario: Admin views table records
- **WHEN** a table record is listed in Django admin or the Django shell
- **THEN** the object label includes the table number and capacity

### Requirement: Reservation time slots are persisted
The system SHALL persist reusable reservation time slots with a start time.

#### Scenario: Admin views time slot records
- **WHEN** a time slot record is listed in Django admin or the Django shell
- **THEN** the object label includes the slot start time

### Requirement: Reservations are persisted
The system SHALL persist reservations with a customer, reservation date, time slot, guest count, and assigned table.

#### Scenario: Admin views reservation records
- **WHEN** a reservation record is listed in Django admin or the Django shell
- **THEN** the object label identifies the customer, date, and assigned table

## REMOVED Requirements

### Requirement: Double-booking is prevented
**Reason**: Complete availability and cancellation rules are outside the introductory Exercise 5 schema.
**Migration**: A later reservation-service exercise will introduce the required business rule and tests.

### Requirement: Smallest-table assignment is supported by schema
**Reason**: Table capacity and guest count remain available, but schema-level ordering and active-state requirements add unnecessary scope at this stage.
**Migration**: Later booking logic can order tables when it implements the assignment workflow.
