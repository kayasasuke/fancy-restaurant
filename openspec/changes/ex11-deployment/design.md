## Decisions

- Render is the selected hosting platform because it supports Python web services and managed PostgreSQL with a simple Blueprint configuration.
- Waitress serves the WSGI application in production, matching the lecture's recommended WSGI deployment approach.
- WhiteNoise serves collected CSS and JavaScript; the application has no user uploads, so media storage is not configured.
- `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, and `DATABASE_URL` are environment-driven. Production must provide a non-development secret key.
- The local default database remains SQLite for course development. Render provides `DATABASE_URL` for PostgreSQL.
- `render.yaml` supplies build, migration, static collection, startup, database, and environment-variable configuration.

## Risks

- A real external deployment cannot be created without access to a Render account. Local production-like verification proves the repository configuration before that account-level step.
