## Why

Exercise 6 returns HTML assembled inside view functions, so repeated page structure and presentation are coupled to request handling. Exercise 7 introduces Django templates and a small, per-browser state boundary before forms and authentication are added in later exercises.

## What Changes

- Render the existing home, table list, time-slot list, reservation placeholder, and reservation detail pages through Django templates.
- Add a shared base template containing the restaurant header, navigation, main content area, and footer.
- Document the separation between persistent reservation data and the future login session state.

## Capabilities

### New Capabilities
- `session-and-template-layout`: Define the Exercise 7 session boundary and reusable Django template structure.

### Modified Capabilities
- `basic-reservation-views`: Existing pages render through templates while preserving their Exercise 6 URLs and responses.

## Impact

- Updates `FancyRestaurantApp` views and adds app-level templates.
- Adds focused template rendering tests.
- Updates README and URL API documentation; no database schema, runtime session write, form, authentication, CSS, or HTMX changes are introduced.
