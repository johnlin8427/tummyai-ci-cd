# Test Coverage Summary

**Overall Coverage: ~72%**

Includes unit, integration, and system tests across core backend modules.

---

## What We Cover

- **Unit tests:** Food model utilities, GCS utilities, error handling
- **Integration tests:** API endpoints (meal history, health report, food-model predict, user list), response validation, error paths
- **System tests:** Server health checks and core HTTP endpoints

---

## What We Skip

- Large model loading (file too large for CI)
- GCS-dependent examples (skipped due to unavailable cloud data in CI)
- Frontend UI tests
- Load/performance testing

---

## CI/CD Integration

- **CI:** Runs linting, builds the container, executes all tests, and enforces a coverage threshold (≥60%)
- **CD:** Builds & deploys via Pulumi and triggers smoke tests

---

## Rationale for Gaps

Model loading + some system tests are skipped only due to CI environment limitations.

Frontend/UI and load testing deprioritized for Milestone 5; can be added later.