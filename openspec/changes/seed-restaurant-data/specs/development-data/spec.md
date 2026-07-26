## ADDED Requirements

### Requirement: Development database can load restaurant inventory
The system SHALL provide a Django fixture that loads reusable restaurant tables and time slots into an empty development database.

#### Scenario: Developer loads initial restaurant data
- **WHEN** a developer runs `python manage.py loaddata initial_restaurant_data`
- **THEN** the database receives tables with seating capacities and selectable evening time slots
