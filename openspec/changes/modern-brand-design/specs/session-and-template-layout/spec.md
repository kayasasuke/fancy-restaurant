## MODIFIED Requirements

### Requirement: Reservation pages share a template layout
The system SHALL render the home, table list, time-slot list, reservation placeholder, and reservation detail pages through app-level Django templates that inherit a common branded base template. The base template SHALL provide a header, navigation, visually grouped main content area, and footer while preserving authenticated and unauthenticated navigation behavior.

#### Scenario: Visitor opens an existing page
- **WHEN** a visitor requests any current HTML page URL
- **THEN** the response uses the shared branded page frame with a header, navigation, grouped main content area, and footer

#### Scenario: Authenticated visitor opens an existing page
- **WHEN** an authenticated customer requests any current HTML page URL
- **THEN** the shared navigation continues to show their login identifier, reservations link, and log-out action

#### Scenario: Page-specific content is rendered from context
- **WHEN** a list or reservation detail page is rendered
- **THEN** its template receives the required database data through the view context and renders it with Django template variables or loops
