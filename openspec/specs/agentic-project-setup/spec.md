# agentic-project-setup Specification

## Purpose
TBD - created by archiving change review-agentic-setup. Update Purpose after archive.
## Requirements
### Requirement: Agent guidance reflects current Django structure
The project SHALL keep agent-facing guidance aligned with the current repository structure, including the `config` Django project and the registered `reservations` app.

#### Scenario: Agent reads project context
- **WHEN** an AI coding agent reads `AGENTS.md`
- **THEN** it sees that `reservations` exists and is registered in `config/settings.py`

### Requirement: Agent setup includes reusable project skills
The project SHALL store reviewed reusable AI skills in `.agents/skills` so future agents can inspect and use project-relevant guidance.

#### Scenario: Skills are installed
- **WHEN** the project agent setup is inspected
- **THEN** `.agents/skills` contains Django, code review, review-response, and refactoring skills

### Requirement: OpenSpec supports spec-driven planning
The project SHALL include OpenSpec project files and OpenCode commands so agent-assisted changes can be planned before implementation.

#### Scenario: OpenSpec is initialized
- **WHEN** OpenSpec setup is inspected
- **THEN** the repository contains `openspec/config.yaml` and OpenCode OpenSpec commands under `.opencode/commands`

### Requirement: Verification commands are explicit
The project SHALL document uv-based verification commands for Django system checks and tests.

#### Scenario: Agent verifies changes
- **WHEN** an AI agent prepares to hand off project changes
- **THEN** it can find `uv run python manage.py check` and `uv run pytest` as the required verification commands

