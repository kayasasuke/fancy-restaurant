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
