# session-and-template-layout Specification

## Purpose
TBD - created by archiving change ex7-sessions-templates. Update Purpose after archive.
## Requirements
### Requirement: Persistent and session state have separate responsibilities
The system SHALL retain customers, restaurant tables, time slots, and reservations in the database. Future login handling SHALL store only the authenticated customer login identifier in the session as temporary per-browser state.

#### Scenario: Exercise 7 state design is documented
- **WHEN** a developer reviews the project state design
- **THEN** it distinguishes database reservation data from the future session login identifier

### Requirement: Reservation pages share a template layout
The system SHALL render the home, table list, time-slot list, reservation placeholder, and reservation detail pages through app-level Django templates that inherit a common base template.

#### Scenario: Visitor opens an existing page
- **WHEN** a visitor requests any current HTML page URL
- **THEN** the response uses the shared page frame with a header, navigation, main content area, and footer

#### Scenario: Page-specific content is rendered from context
- **WHEN** a list or reservation detail page is rendered
- **THEN** its template receives the required database data through the view context and renders it with Django template variables or loops
