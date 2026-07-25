## Why

The reservation page still submits a hard-coded sample booking, so it cannot represent a real visitor's reservation request. Exercise 8 replaces that stub with the first validated Django form while keeping the interface intentionally simple.

## What Changes

- Add a Django form for customer name, guest count, reservation date, and a database-backed time-slot choice.
- Submit the form with POST to the existing reservation URL and show field errors without creating a reservation.
- Create a guest customer and reservation on valid input, assigning the smallest suitable existing table before redirecting to the detail page.
- Remove the obsolete hard-coded sample-creation URL.

## Capabilities

### New Capabilities
- `reservation-form-input`: Define validated reservation input and the first guest booking submission workflow.

### Modified Capabilities
- `basic-reservation-views`: Replace the placeholder reservation form and sample-creation URL with the real form workflow.

## Impact

- Adds `FancyRestaurantApp/forms.py` and updates the reservation view, URLs, template, and tests.
- Updates the documented URL API and form behavior.
- Does not add database migrations, registration, login, password handling, HTMX, CSS, or alternative availability suggestions.
