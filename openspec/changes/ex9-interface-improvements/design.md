## Context

Exercise 8 supplies working templates and a reservation form. The instructor repository has a static stylesheet, but its reset and later HTMX-oriented interface are beyond the Exercise 9 scope. The lecture asks for an external stylesheet, semantic HTML, responsive design, and accessibility basics.

## Decisions

- Place one stylesheet at `FancyRestaurantApp/static/FancyRestaurantApp/style.css` and load it with Django's `static` template tag from `base.html`.
- Keep the current header, navigation, main, footer, headings, links, form labels, and button semantics. Add classes only to identify reusable visual roles.
- Use a readable neutral palette with high-contrast text, a visible `:focus-visible` outline, and distinct error text.
- Use a modest `max-width` page container and one small media query to stack the navigation and preserve usable spacing on narrow screens.
- Keep browser-native form controls and Django-rendered labels; no component library or JavaScript is needed.

## Non-Goals

- Do not create a new design system, add images, or redesign the booking workflow.
- Do not add HTMX, inline styles, client-side validation, authentication, or date availability logic.
