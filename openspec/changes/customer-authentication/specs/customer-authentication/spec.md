## ADDED Requirements

### Requirement: Visitor can register a customer account
The system SHALL allow a visitor to register a customer name, unique login, and password.

#### Scenario: Visitor registers valid account data
- **WHEN** a visitor submits a unique login with matching valid passwords
- **THEN** the system creates a customer with a hashed password, records the login in the session, and redirects home

#### Scenario: Visitor submits invalid registration data
- **WHEN** a visitor submits a duplicate login or mismatched passwords
- **THEN** the system re-renders the registration form with errors and creates no customer

### Requirement: Registered customer can authenticate
The system SHALL allow a registered customer to log in and log out through session-backed authentication.

#### Scenario: Customer logs in successfully
- **WHEN** a customer submits a registered login and correct password
- **THEN** the system stores the login in the session and redirects home

#### Scenario: Customer submits invalid credentials
- **WHEN** a customer submits an unknown login or an incorrect password
- **THEN** the system re-renders the login form with an error and does not authenticate the session

#### Scenario: Customer logs out
- **WHEN** an authenticated customer sends a POST request to the logout URL
- **THEN** the system clears the authenticated login from the session and redirects home

### Requirement: Authenticated reservation uses existing customer
The system SHALL assign a new reservation to the authenticated customer rather than creating another guest customer.

#### Scenario: Authenticated customer opens the reservation form
- **WHEN** an authenticated customer requests the new-reservation page
- **THEN** the form shows their name as read-only

#### Scenario: Authenticated customer submits a valid reservation
- **WHEN** an authenticated customer submits a valid reservation
- **THEN** the system creates the reservation for the authenticated customer and creates no new customer

### Requirement: Authenticated customer can view their reservations
The system SHALL show an authenticated customer only the reservations assigned to their customer record.

#### Scenario: Authenticated customer opens their reservation list
- **WHEN** an authenticated customer requests the reservation-list URL
- **THEN** the system returns their reservations ordered by date and time

#### Scenario: Anonymous visitor opens the reservation list
- **WHEN** an anonymous visitor requests the reservation-list URL
- **THEN** the system redirects them to the login page

### Requirement: Reservation date and time are not in the past
The system SHALL reject a reservation date before the restaurant's `Asia/Tokyo` local current date and a time slot that has already begun today.

#### Scenario: Customer submits a past reservation date
- **WHEN** a customer submits a reservation date before today
- **THEN** the reservation form shows a validation error and creates no reservation

#### Scenario: Availability is checked for a past reservation date
- **WHEN** the availability endpoint receives a reservation date before today
- **THEN** it returns no availability result

#### Scenario: Customer submits an elapsed time slot today
- **WHEN** a customer submits today's time slot at or before the restaurant's current local time
- **THEN** the reservation form shows a validation error and creates no reservation

#### Scenario: Availability is checked for an elapsed time slot today
- **WHEN** the availability endpoint receives today's time slot at or before the restaurant's current local time
- **THEN** it returns no availability result
