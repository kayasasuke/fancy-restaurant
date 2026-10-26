## Context

The application has a shared Django base template and one small external stylesheet. Its functionality is complete for the current reservation workflow, but the visual presentation is intentionally bare. The redesign must preserve the template inheritance and all existing form and session behavior.

## Goals / Non-Goals

**Goals:**

- Establish a modern, cohesive visual language using the supplied navy, blue, periwinkle, and lavender palette.
- Make navigation, primary actions, form controls, feedback, and reservation information easy to scan on desktop and mobile.
- Retain visible keyboard focus and readable validation errors.

**Non-Goals:**

- Adding new booking features, routes, JavaScript interactions, imagery, external fonts, or dependencies.
- Changing database models, form fields, or authentication/session behavior.

## Decisions

- Use CSS custom properties for the five supplied palette colors plus accessible derived neutrals. This keeps the brand system centralized and avoids repeated literal values.
- Give the base template a compact branded top bar and a centered content card. This improves hierarchy consistently across all inherited views without duplicating markup. A page-by-page redesign was considered, but it would be less consistent and more fragile.
- Add semantic utility classes only where the shared layout or repeated information groups need structured styling. Existing Django-generated form markup remains intact so validation and behavior are preserved.
- Use responsive CSS grid and flexible layout rules rather than a UI framework. This avoids adding dependencies and maintains the current lightweight Django stack.

## Risks / Trade-offs

- [Strong color contrast can make text difficult to read] → Use the navy for primary text, white text only on dark surfaces, and retain a high-visibility focus ring.
- [Django `form.as_p` creates generic markup] → Style form elements and paragraphs directly, with narrow scoped selectors.
- [Shared template changes affect all screens] → Verify the home, forms, lists, and details via automated checks and a visual browser pass.

## Migration Plan

Deploy the template and stylesheet changes together; no data migration or configuration change is required. Rollback consists of restoring the prior template and stylesheet revision.

## Open Questions

None. The supplied palette and the existing route behavior provide sufficient direction.
