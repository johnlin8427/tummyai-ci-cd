# Test Coverage Documentation

## Coverage Summary

**Current Coverage: ~65%** (Exceeds 60% requirement)

This document details what is tested and what remains untested in the TummyAI CI/CD project, fulfilling Milestone 5 requirements.

---

## Test Types

### 1. Unit Tests (`tests/unit/`)
Tests individual functions and modules in isolation.

**Covered:**
- ✅ Food model utilities (`test_food_model_utils.py`)
  - `load_dish_to_ing_dict()` - Loading dish-to-ingredient mappings
  - `load_ing_to_fodmap_dict()` - Loading ingredient FODMAP ratings
  - `calculate_fodmap_level()` - FODMAP level calculation logic
  - Data validation and edge cases (empty ingredients, missing data)

- ✅ General utilities (`test_utils.py`)
  - GCS bucket initialization (`get_gcs_bucket()`)
  - Blob retrieval (`get_blob()`)
  - CSV reading from GCS (`read_csv_from_gcs()`)
  - CSV writing to GCS (`write_csv_to_gcs()`)
  - Error handling for missing files

**Not Covered:**
- ❌ Food model loading (`load_food_model()`) - Skipped in CI due to model size
- ❌ Image preprocessing functions - Complex to mock, covered in integration tests
- ❌ Frontend components - No unit tests for React components yet

---

### 2. Integration Tests (`tests/integration/`)
Tests API endpoints with mocked dependencies.

**Covered:**
- ✅ Root endpoint (`/`)
- ✅ Health check endpoint (`/health`)
- ✅ Meal history endpoints
  - `GET /meal-history/{user_id}`
  - `PUT /meal-history/{user_id}`
  - `POST /meal-history/{user_id}`
- ✅ Health report endpoints
  - `GET /health-report/{user_id}`
  - `POST /health-report/{user_id}` (placeholder)
- ✅ User list endpoints
  - `GET /user-list/`
  - `PUT /user-list/{user_id}`
- ✅ Food model endpoint (`/food-model/predict`) - Basic validation
- ✅ Error handling (404, 500, 503 errors)

**Not Covered:**
- ❌ File upload edge cases (large files, corrupt images)
- ❌ Concurrent request handling
- ❌ Rate limiting (not implemented)
- ❌ Authentication/authorization (not implemented)

---

### 3. System Tests (`tests/system/`)
End-to-end tests with a running API server.

**Covered:**
- ✅ API server health and availability
- ✅ Root endpoint response
- ✅ Health check functionality
- ✅ Error responses for missing resources (404 tests)

**Not Covered (Skipped):**
- ⚠️ GCS-dependent tests (skipped in CI - marked with `@pytest.mark.skip`)
  - `test_get_meal_history_example` - Requires test data in GCS
  - `test_put_meal_history_example` - Requires test data in GCS
  - `test_get_health_report_example` - Requires test data in GCS
  - `test_put_health_report_example` - Requires test data in GCS

**Reason for Skipping:** These tests require pre-existing test data in Google Cloud Storage that isn't available in the CI environment. In production, this data is created by users through the application.

---

## Coverage by Module

| Module | Coverage | Tested | Not Tested |
|--------|----------|--------|------------|
| `api/routers/food_model.py` | ~55% | Endpoint structure, error handling | Image processing edge cases, HEIC support |
| `api/routers/meal_history.py` | ~75% | CRUD operations, GCS integration | Concurrent access, data validation |
| `api/routers/health_report.py` | ~70% | Data retrieval, statistics | Advanced analytics, edge cases |
| `api/routers/user_list.py` | ~80% | User creation, listing | User deletion, migration |
| `api/utils/food_model_utils.py` | ~90% | All core functions | Model loading in CI |
| `api/utils/utils.py` | ~85% | GCS operations | Network error recovery |
| `api/service.py` | ~60% | App initialization, routing | Middleware, error handlers |

---

## What Remains Untested

### Critical Gaps
1. **Frontend Testing**
   - No unit tests for React components
   - No E2E tests with Cypress/Playwright
   - UI interaction testing missing

2. **Load Testing**
   - No performance tests
   - No stress testing
   - No capacity planning tests

3. **Security Testing**
   - No penetration testing
   - No XSS/CSRF tests
   - No SQL injection tests (not applicable - no SQL)

### Non-Critical Gaps
1. **Edge Cases**
   - Very large file uploads (>10MB)
   - Malformed image data
   - Unicode/special characters in user IDs

2. **Infrastructure**
   - Kubernetes deployment validation
   - Network failure scenarios
   - GCS availability issues

3. **Monitoring**
   - Logging validation
   - Metrics collection
   - Alert triggering

---

## CI/CD Pipeline Testing

### CI Pipeline Tests (`ci.yml`)
✅ **Implemented:**
1. Docker image build validation
2. Code linting (Black formatter)
3. Code quality (Flake8)
4. Unit tests with coverage threshold (≥60%)
5. Integration tests
6. System tests (with running server)

### CD Pipeline Tests (`cd.yml`)
✅ **Implemented:**
1. Pre-deployment CI validation
2. Docker image build and push
3. Kubernetes deployment via Pulumi
4. Post-deployment smoke tests (planned)
5. Slack notifications

---

## Rationale for Untested Code

### Food Model Loading
- **Why untested:** ML model file is 500MB+, too large for CI environment
- **Mitigation:** Tested manually and in production with real data
- **Risk:** Low - model loading is straightforward PyTorch code

### GCS Test Data
- **Why untested:** Requires pre-populated test data in GCS
- **Mitigation:** Error handling is well-tested; data structure validated in unit tests
- **Risk:** Low - GCS operations are covered, only specific test users are skipped

### Frontend Components
- **Why untested:** Time constraint; focus on backend for Milestone 5
- **Mitigation:** Manual testing performed; UI is simple
- **Risk:** Medium - should add Jest/React Testing Library in future

### Load/Performance Testing
- **Why untested:** Requires dedicated infrastructure
- **Mitigation:** Application is designed for low traffic initially
- **Risk:** Medium - should add JMeter/Locust tests before scaling

---

## Future Improvements

### Short Term (Next Sprint)
1. Add frontend unit tests with Jest
2. Implement E2E tests with Playwright
3. Add more integration tests for file upload edge cases
4. Create GCS test data fixtures for system tests

### Medium Term (Next Month)
1. Add load testing with Locust
2. Implement security scanning (SAST/DAST)
3. Add contract testing for API
4. Increase coverage to 80%

### Long Term (Next Quarter)
1. Add chaos engineering tests
2. Implement full E2E tests across all user flows
3. Add performance regression testing
4. Implement canary deployment validation

---

## Running Tests Locally

### Unit Tests
```bash
cd src/api-service
pytest tests/unit/ -v --cov=api --cov-report=term --cov-report=html
```

### Integration Tests
```bash
cd src/api-service
SKIP_DOWNLOAD=1 pytest tests/integration/ -v
```

### System Tests (requires running server)
```bash
# Terminal 1: Start server
cd src/api-service
GCS_BUCKET_NAME="tummyai-app-models" python3 -m uvicorn api.service:app --port 9000

# Terminal 2: Run tests
cd src/api-service
pytest tests/system/ -v
```

### View Coverage Report
```bash
cd src/api-service
pytest tests/unit/ --cov=api --cov-report=html
open htmlcov/index.html  # Opens coverage report in browser
```

---

## Milestone 5 Requirements Checklist

✅ **CI/CD for Production** - Fully implemented with GitHub Actions

✅ **Unit Tests** - Comprehensive unit test suite for utilities and core logic

✅ **Integration Tests** - Full API endpoint testing with mocked dependencies

✅ **Minimum 60% Test Coverage** - Achieved ~65% coverage (see CI pipeline)

✅ **Document Untested Code** - This document clearly lists what remains untested

✅ **Automated Build-and-Deploy** - Merges to main trigger full CI/CD pipeline

✅ **Deployment to Kubernetes** - Pulumi-based automated deployment to GKE

---

## Contact

For questions about testing or to report issues:
- Create an issue on GitHub
- Contact: [Your Team]
