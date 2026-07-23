## Purpose
Define the initial Django database schema for the restaurant reservation domain.

## Requirements

### Requirement: Restaurant tables are persisted
The system SHALL persist restaurant tables with a table number, seating capacity, and active status.

#### Scenario: Admin views table records
- **WHEN** a table record is listed in Django admin or the Django shell
- **THEN** the object label includes the table number and capacity

### Requirement: Reservation time slots are persisted
The system SHALL persist reusable reservation time slots with a start time, duration, and active status, and active time slots MUST not overlap.

#### Scenario: Admin views time slot records
- **WHEN** a time slot record is listed in Django admin or the Django shell
- **THEN** the object label includes the slot start time

#### Scenario: Overlapping active time slot is validated
- **WHEN** an active time slot overlaps an existing active time slot
- **THEN** model validation rejects the overlapping time slot

### Requirement: Reservations are persisted
The system SHALL persist reservations with customer identity, reservation date, time slot, guest count, assigned table, and status.

#### Scenario: Admin views reservation records
- **WHEN** a reservation record is listed in Django admin or the Django shell
- **THEN** the object label identifies the customer, date, time slot, and assigned table

### Requirement: Double-booking is prevented
The system SHALL prevent the same table from being reserved twice for the same date and time slot by active reservations.

#### Scenario: Duplicate table reservation is saved
- **WHEN** a second reservation uses the same table, reservation date, and time slot as an existing reservation
- **THEN** the database rejects the duplicate reservation

#### Scenario: Cancelled table reservation is replaced
- **WHEN** an existing reservation for a table, date, and time slot is cancelled
- **THEN** a new active reservation can use the same table, date, and time slot

### Requirement: Smallest-table assignment is supported by schema
The system SHALL store table capacity and reservation guest count so later booking logic can select the smallest active table that fits a party.

#### Scenario: Tables are queried for assignment
- **WHEN** table records are ordered by capacity and table number
- **THEN** smaller suitable tables appear before larger suitable tables
