# Capabilities

This folder defines all runtime capabilities and their execution policies.

- Each capability has:
  - `handler` - The function executed.
  - `policy` - Retry, failure, and dependency rules.
  - `description` - Human-readable description.

- Runtime dependency enforcement ensures capabilities only execute when required data exists.
- Degraded continuation allows partial execution in recoverable failures.

