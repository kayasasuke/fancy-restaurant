## ADDED Requirements

### Requirement: Restaurant tables are persisted
The system SHALL persist restaurant tables with a table number, seating capacity, and active status.

#### Scenario: Admin views table records
- **WHEN** a table record is listed in Django admin or the Django shell
- **THEN** the object label includes the table number and capacity

### Requirement: Reservation time slots are persisted
The system SHALL persist reusable reservation time slots with a start time, duration, and active status.

#### Scenario: Admin views time slot records
- **WHEN** a time slot record is listed in Django admin or the Django shell
- **THEN** the object label includes the slot start time

### Requirement: Reservations are persisted
The system SHALL persist reservations with customer identity, reservation date, time slot, guest count, assigned table, and status.

#### Scenario: Admin views reservation records
- **WHEN** a reservation record is listed in Django admin or the Django shell
- **THEN** the object label identifies the customer, date, time slot, and assigned table

### Requirement: Double-booking is prevented
The system SHALL prevent the same table from being reserved twice for the same date and time slot.

#### Scenario: Duplicate table reservation is saved
- **WHEN** a second reservation uses the same table, reservation date, and time slot as an existing reservation
- **THEN** the database rejects the duplicate reservation

### Requirement: Smallest-table assignment is supported by schema
The system SHALL store table capacity and reservation guest count so later booking logic can select the smallest active table that fits a party.

#### Scenario: Tables are queried for assignment
- **WHEN** table records are ordered by capacity and table number
- **THEN** smaller suitable tables appear before larger suitable tables
