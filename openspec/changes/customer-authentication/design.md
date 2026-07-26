## Context

The instructor project uses custom patient registration and login forms, hashes passwords with Django helpers, and stores an authorized login in the session. This project has the same planned `Customer` fields but no authentication workflow yet.

## Decisions

- Keep `Customer` as the domain customer record rather than introducing Django's built-in auth model.
- Add `RegistrationForm` with name, login, password, and password confirmation; reject duplicate non-empty logins and mismatched passwords.
- Hash passwords with `make_password` and authenticate with `check_password`; never store or render plain passwords.
- Store only `authorized_customer_login` in the session. On each use, resolve the current `Customer`; clear stale session state when it no longer resolves.
- Add `LoginForm`, `registration`, `login`, and POST-only `logout` views. Successful registration and login redirect to the home page.
- Pass the authenticated customer into `ReservationForm` to display a read-only name, but choose the authenticated customer server-side when creating a reservation.
- Existing guest bookings remain guest records. A customer must register to use future authenticated bookings; name matching alone is not a safe account migration method.

## Non-Goals

- No password recovery, email, account deletion, permissions, or conversion of existing guest customers.
