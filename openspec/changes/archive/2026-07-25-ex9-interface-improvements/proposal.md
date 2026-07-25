## Why

The reservation pages use semantic templates but have no project stylesheet, responsive layout, or explicit keyboard focus treatment. Exercise 9 improves the existing interface without changing reservation behavior.

## What Changes

- Add one app-level CSS file and load it from the shared base template.
- Use restrained styles for the page layout, navigation, forms, lists, reservation details, and buttons.
- Add a viewport declaration, responsive navigation, visible focus states, and readable validation messages.
- Make small semantic template adjustments only where they improve the existing page structure.

## Out Of Scope

- HTMX, JavaScript, authentication, new pages, images, animations, or changes to reservation logic.

## Impact

- Updates the shared base template and small existing page templates.
- Adds static CSS and focused template tests.
