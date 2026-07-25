## Context

The lecture and instructor example attach `hx-post` and `hx-target` attributes to selected Django form widgets, then return a small fragment from a read-only availability view. The instructor's broader login and event-driven UI is later scope.

## Decisions

- Add `django-htmx` to Django settings and middleware, and serve a local `htmx.min.js` static asset as shown in the lecture.
- Add `hx-post`, `hx-target`, and `hx-include="closest form"` to the guest-count, date, and time-slot widgets. Their normal change event triggers the check while retaining the ordinary form submission behavior.
- Add `POST /reservations/availability/` with a `reservation-availability` URL name. It validates only the values relevant to table availability and makes no database writes.
- Render `availability_result.html` into `#availability-result`, which has `aria-live="polite"`.
- For complete valid availability input, return either the smallest available table or a no-table message. For incomplete or invalid availability fields, return an empty fragment to avoid premature errors while the visitor is editing.

## Non-Goals

- Do not make the final form submit through HTMX or change its redirect behavior.
- Do not calculate alternate slots, alter the schema, introduce custom events, or add JavaScript beyond HTMX itself.
