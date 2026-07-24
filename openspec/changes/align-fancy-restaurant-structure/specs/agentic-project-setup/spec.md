## MODIFIED Requirements

### Requirement: Agent guidance reflects current Django structure
The project SHALL keep agent-facing guidance aligned with the current repository structure, including the `FancyRestaurant` Django project and the registered `FancyRestaurantApp` app with the stable `reservations` label.

#### Scenario: Agent reads project context
- **WHEN** an AI coding agent reads `AGENTS.md`
- **THEN** it sees that `FancyRestaurantApp` implements the reservation domain and is registered in `FancyRestaurant/settings.py`
