## Context

The repository is a uv-managed Django project for restaurant reservations. It has a `config` Django project, a registered `reservations` app, `AGENTS.md`, OpenCode installed locally, OpenSpec initialized for OpenCode, and project skills installed under `.agents/skills`.

The current `AGENTS.md` still says no Django apps exist, which no longer matches the repository. The AI setup also needs to make the lecture workflow visible: project context in `AGENTS.md`, reusable skills under `.agents/skills`, OpenSpec slash commands under `.opencode/commands`, and verification through `manage.py check` plus pytest.

## Goals / Non-Goals

**Goals:**
- Keep `AGENTS.md` accurate for the current Django project structure.
- Preserve the generated OpenSpec and OpenCode setup.
- Document the installed skills and the expected verification workflow.
- Keep business-code behavior untouched.

**Non-Goals:**
- Do not add reservation models, views, URLs, templates, migrations, or business logic.
- Do not configure GitHub MCP or issue/PR automation in this change.
- Do not push to GitHub until the setup is reviewed and committed.

## Decisions

- Use OpenCode as the primary installed coding agent because it matches the lecture recommendation and is already available locally.
- Initialize OpenSpec for OpenCode so slash commands and OpenSpec skills live in `.opencode/`.
- Keep skills in `.agents/skills` because the lecture recommends committing reviewed project skills there.
- Update `AGENTS.md` directly rather than creating another agent-specific root instruction file, because the project already uses `AGENTS.md` as its shared agent context.

## Risks / Trade-offs

- External skills can contain broad instructions or assumptions that do not fit this project. Mitigation: keep them committed as readable markdown and review before relying on them.
- OpenSpec Codex setup failed because `.codex` creation was blocked in this sandbox. Mitigation: OpenCode setup succeeded, and the project still has OpenSpec CLI plus OpenCode commands.
- OpenSpec telemetry is enabled by default. Mitigation: users can opt out with `OPENSPEC_TELEMETRY=0` when running OpenSpec commands.
