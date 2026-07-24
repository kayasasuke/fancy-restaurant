## Why

Exercise 6 requires the Django project to start becoming a working web application by adding basic view functions and connecting them to URLs. The reservation app currently has database models but no callable user-facing pages or actions.

## What Changes

- Add simple function-based views for the main reservation user actions.
- Add an app-level URL configuration and include it from the project URL configuration.
- Use basic `HttpResponse` output, redirects, and small ORM queries in line with the lecture material.
- Add tests for the callable URLs, response status codes, visible content, redirects, object creation, and 404 behavior.
- Update README documentation with the current URL API, URL arguments, and return values.

## Capabilities

### New Capabilities

- `basic-reservation-views`: Defines the first callable URLs and simple Django views for the reservation app.

### Modified Capabilities

- None.

## Impact

- Affects `reservations/views.py`, a new `reservations/urls.py`, `config/urls.py`, tests, README, and OpenSpec change artifacts.
- Does not introduce templates, forms, authentication, complete booking logic, or external dependencies.
