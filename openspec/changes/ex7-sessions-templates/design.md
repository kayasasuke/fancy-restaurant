## Context

The Exercise 6 views return HTML assembled with Python strings. Django already has session middleware and app template discovery enabled. The instructor repository demonstrates session access with `request.session` and a base template, but its current code also includes forms, authentication, HTMX, static assets, and later-course workflows.

## Goals / Non-Goals

**Goals:**

- Separate the existing page markup from the view functions with app-level templates.
- Provide one shared layout for every current reservation page.
- Make the database/session boundary explicit without introducing a premature session workflow.

**Non-Goals:**

- Add registration, login, password handling, Django forms, CSS, HTMX, or a complete booking workflow.
- Move `Customer`, `Reservation`, `Table`, or `TimeSlot` records into session storage.
- Change the Exercise 5 database schema or add migrations.

## Decisions

- Use app-namespaced templates under `FancyRestaurantApp/templates/FancyRestaurantApp/`.
  - Django discovers them through the existing `APP_DIRS` configuration and namespacing prevents future app template collisions.
  - A project-wide template directory is unnecessary for one app at this course stage.

- Use `base.html` with `title` and `content` blocks for the header, navigation, main content, and footer.
  - All current pages share this frame; individual templates supply only page-specific markup.
  - Styling and static assets are deferred to later exercises.

- Reserve session storage for the authenticated customer's login identifier in the later login exercise.
  - The hard-coded Ex6 sample reservation has no user input or authentication, so storing its name would create state with no user-facing purpose.
  - `Customer`, reservation details, table availability, and time slots remain database data because they are shared and persistent.

## Risks / Trade-offs

- [A future login session becomes stale after customer data changes] -> Store only an identifier and query the database for authoritative customer data.
- [Template updates can change existing response text] -> Preserve current headings and test each existing URL and template.
- [Teacher implementation includes later-exercise features] -> Deliberately limit this change to the course's session/template concepts.

## Migration Plan

1. Add templates and convert the existing views to `render()` without changing URLs.
2. Document the future session key and database/session boundary.
3. Verify the template behavior with Django tests.
4. Roll back by restoring the prior views; no database migration or persistent data conversion is required.
