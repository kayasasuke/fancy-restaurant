## ADDED Requirements

### Requirement: Modern branded reservation interface
The system SHALL present existing reservation pages with a cohesive modern interface that uses `#141B41`, `#306BAC`, `#6F9CEB`, `#98B9F2`, and `#918EF4` as its brand palette.

#### Scenario: Visitor opens a reservation page
- **WHEN** a visitor opens the home page, a reservation form, a reservation list, or a reservation detail page
- **THEN** the shared interface presents a branded header, visually grouped primary content, and a consistent footer using the supplied palette

### Requirement: Responsive reservation presentation
The system SHALL adapt navigation, content panels, forms, and primary actions for narrow viewports without horizontal overflow.

#### Scenario: Visitor uses a narrow viewport
- **WHEN** a visitor views any reservation page on a narrow screen
- **THEN** the page preserves readable spacing, controls fit the viewport, and navigation remains usable

### Requirement: Accessible interaction feedback
The system SHALL retain visibly distinguishable form errors and keyboard focus states in the branded interface.

#### Scenario: Visitor uses keyboard navigation
- **WHEN** a visitor focuses a link, input, select, or button using the keyboard
- **THEN** the focused control has a visible high-contrast focus indicator

#### Scenario: Visitor submits invalid form data
- **WHEN** a visitor submits invalid login, registration, or reservation input
- **THEN** validation errors are visually distinct from ordinary page text
