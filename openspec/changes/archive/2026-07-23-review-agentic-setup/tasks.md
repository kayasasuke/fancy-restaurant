## 1. Tooling Setup

- [x] 1.1 Confirm OpenCode is installed and available for the project.
- [x] 1.2 Install OpenSpec and initialize it for OpenCode.
- [x] 1.3 Install the recommended project skills under `.agents/skills`.

## 2. Project Guidance

- [x] 2.1 Update `AGENTS.md` so it reflects the existing `reservations` Django app.
- [x] 2.2 Add concise project context to `openspec/config.yaml`.
- [x] 2.3 Confirm generated agent files are project-specific and do not include generated Python bytecode or runtime artifacts.

## 3. Verification

- [x] 3.1 Run `openspec doctor`.
- [x] 3.2 Run `uv run python manage.py check`.
- [x] 3.3 Run `uv run pytest`.
- [x] 3.4 Review `git status --short --branch` before handoff.
