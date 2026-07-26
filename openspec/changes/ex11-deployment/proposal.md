## Why

The project currently uses development-only Django settings, SQLite, and Django's development static-file server. Exercise 11 requires a documented, deployable production configuration.

## What Changes

- Use Render for hosting, PostgreSQL for production data, Waitress as the WSGI application server, and WhiteNoise for static files.
- Read production configuration and secrets from environment variables.
- Add a Render Blueprint and deployment documentation.
- Verify static collection and a local production-like Waitress run.

## Out Of Scope

- User-uploaded media files, custom domains, HTTPS configuration, and creating a user-owned Render account.
