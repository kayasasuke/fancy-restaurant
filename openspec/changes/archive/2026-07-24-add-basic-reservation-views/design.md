## Context

The project has a Django `reservations` app with `Table`, `TimeSlot`, and `Reservation` models. It does not yet expose any user-facing URLs except Django admin. Lecture 6 introduces function-based views, `HttpResponse`, URL mapping with `path()`, redirects, and simple ORM reads/writes from views.

## Goals / Non-Goals

**Goals:**

- Implement several small function-based views representing clear user actions or pages.
- Connect app URLs through `reservations/urls.py` and `config/urls.py`.
- Keep output simple and inspectable with plain text/HTML responses.
- Include one redirecting view and one simple database-writing view.
- Document the current callable URL API.

**Non-Goals:**

- Build final HTML templates or CSS.
- Build complete reservation availability and suggestion logic.
- Add login, registration, full forms, or POST/CSRF workflows.
- Add REST Framework or class-based views.

## Decisions

- Use function-based views and `HttpResponse`.
  - Rationale: this matches the lecture and keeps Exercise 6 focused on request/response basics.
  - Alternative considered: Django templates. Templates are useful soon, but would add a second concept before the view/URL mapping is established.

- Add `reservations/urls.py` and include it from `config/urls.py`.
  - Rationale: app-owned URL configuration keeps the reservation app modular.
  - Alternative considered: place all routes in `config/urls.py`. That is acceptable for tiny examples but scales poorly.

- Use a small hard-coded sample reservation creation view.
  - Rationale: the exercise allows hard-coded user-supplied values and asks for basic actions, not a final form processor.
  - Alternative considered: accepting GET/POST inputs now. That belongs in a later form exercise.

- Use `select_related()` when showing reservation details.
  - Rationale: reservation detail needs the related table and time slot; this avoids unnecessary extra queries.

## Risks / Trade-offs

- Plain HTML strings are not production UI -> README will document that these are temporary basic views.
- The sample creation view writes data through GET -> acceptable for this exercise demonstration, but a later form/POST implementation should replace it.
- Hard-coded sample data may fail if default table or slot conflicts exist -> the view will create or reuse known records and cancel an existing sample reservation before creating a replacement.
