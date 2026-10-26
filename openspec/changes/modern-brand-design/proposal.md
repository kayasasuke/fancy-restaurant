## Why

The reservation flow is functional but currently has only a minimal utility style. A cohesive visual identity will make the service feel more polished and easier to scan without changing how customers book or manage reservations.

## What Changes

- Refresh the shared page layout and responsive styling with a modern restaurant-reservation visual system.
- Use the requested brand palette: `#141B41`, `#306BAC`, `#6F9CEB`, `#98B9F2`, and `#918EF4`.
- Improve the hierarchy and presentation of navigation, forms, buttons, status messages, lists, and reservation details.
- Preserve all existing routes, form fields, session behavior, and reservation functionality.

## Capabilities

### New Capabilities
- `modern-reservation-interface`: A responsive, accessible branded interface for the reservation experience.

### Modified Capabilities

- `session-and-template-layout`: The shared template layout gains an enhanced visual shell while preserving its navigation and authenticated-state behavior.

## Impact

- Affected code: shared CSS and Django templates in `FancyRestaurantApp`.
- No API, database, dependency, or reservation-rule changes.
