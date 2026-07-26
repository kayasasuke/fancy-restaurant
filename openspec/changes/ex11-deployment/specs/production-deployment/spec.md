## ADDED Requirements

### Requirement: Production settings use environment configuration
The system SHALL read production secrets and deployment configuration from environment variables.

#### Scenario: Production configuration has the required values
- **WHEN** the application starts with production settings and required environment variables
- **THEN** it uses the supplied secret key, allowed hosts, and database URL

#### Scenario: Production configuration is missing a secret key
- **WHEN** the application starts with debug disabled and no non-development secret key
- **THEN** startup fails without using the development key

### Requirement: Static files are deployable
The system SHALL collect and serve static files in production.

#### Scenario: Static files are collected
- **WHEN** the deployment build runs `collectstatic`
- **THEN** CSS and JavaScript are written to the configured static root

### Requirement: Deployment is documented
The project SHALL document its Render deployment platform, application server, static-file strategy, environment variables, database, media-file policy, and deployment commands.

#### Scenario: Developer follows the deployment documentation
- **WHEN** a developer prepares a Render deployment
- **THEN** the README provides dependency, migration, static collection, and startup commands
