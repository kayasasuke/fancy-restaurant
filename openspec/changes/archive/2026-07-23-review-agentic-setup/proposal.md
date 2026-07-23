## Why

The project now has a Django skeleton, a registered `reservations` app, OpenCode, OpenSpec, and project skills, but the agent-facing context needs to reflect that current state. Keeping this setup accurate helps future AI-assisted changes reuse the right Django structure and verification flow.

## What Changes

- Review the current AI-agent setup against the lecture workflow.
- Update project guidance so it no longer claims no Django apps exist.
- Record the expected AI setup, including OpenCode, OpenSpec, project skills, and uv-based verification commands.
- Keep the change limited to agentic setup documentation and OpenSpec planning artifacts.

## Capabilities

### New Capabilities
- `agentic-project-setup`: Documents the expected AI-agent setup and workflow for this Django reservation project.

### Modified Capabilities

## Impact

- Affected files are limited to `AGENTS.md`, OpenSpec project files, OpenCode command/skill files, and installed skill files under `.agents/skills`.
- No Django models, views, URLs, migrations, or runtime reservation behavior should change.
