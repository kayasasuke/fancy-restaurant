## Why

Visitors currently learn whether a reservation is possible only after submitting the full form. Exercise 10 adds one partial-page availability check while preserving the existing server-rendered reservation workflow.

## What Changes

- Configure `django-htmx` and load the HTMX client library from app static files.
- Trigger an availability query when the party size, date, or time slot changes.
- Replace one result region with a server-rendered availability fragment.
- Keep the final reservation POST and all database writes in the existing view.

## Out Of Scope

- HTMX reservation creation, login, registration, custom events, alternative-time suggestions, and client-side business rules.
