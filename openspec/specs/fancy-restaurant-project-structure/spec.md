## Purpose
Define the canonical Django project and app package structure for Fancy Restaurant.

## Requirements

### Requirement: The Django packages identify the Fancy Restaurant project
The system SHALL use `FancyRestaurant` as its Django project package and `FancyRestaurantApp` as its reservation-domain Django app package.

#### Scenario: Django loads the project
- **WHEN** a developer runs a Django management command or pytest
- **THEN** Django loads settings from `FancyRestaurant.settings` and imports `FancyRestaurantAppConfig`

### Requirement: Existing reservation migrations remain compatible
The reservation-domain Django app MUST retain the `reservations` application label while its Python package is named `FancyRestaurantApp`.

#### Scenario: Existing migrations are inspected
- **WHEN** Django checks the reservation app migration state
- **THEN** it recognizes the existing `reservations` migration history without creating a second set of reservation tables

### Requirement: Customer reservation identity is documented
The project documentation SHALL state that the restaurant domain uses its own `Customer` record, corresponding to the instructor example's `Patient` model.

#### Scenario: Developer reviews the schema
- **WHEN** a developer reads the project schema documentation
- **THEN** they can identify how a customer and reservation are represented

### Requirement: Agent guidance reflects the completed project state
The project SHALL keep AGENTS.md aligned with the completed Django models, views, URLs, tests, and tool configuration.

#### Scenario: Agent reads project context
- **WHEN** an AI coding agent reads AGENTS.md
- **THEN** it sees the current FancyRestaurant and FancyRestaurantApp structure and does not receive obsolete implementation status
