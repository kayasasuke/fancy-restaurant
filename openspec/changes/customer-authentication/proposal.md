## Why

Every current reservation creates a guest customer record, so a returning customer cannot authenticate or reuse an existing record. The existing `Customer` model already has login and password fields for this planned behavior.

## What Changes

- Add registration, login, and logout forms and URLs using the existing `Customer` model.
- Hash passwords on registration and use session state to remember the authenticated login.
- Prefill the reservation name for an authenticated customer and assign new reservations to that existing customer.
- Add navigation links and document the authentication URLs.

## Out Of Scope

- Password reset, email verification, Django's built-in user model, social authentication, authorization roles, and automatic conversion of historical guest bookings.
