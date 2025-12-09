# GitHub Actions CI/CD Pipelines

This directory contains automated CI/CD workflows for the TummyAI project.

## Workflows Overview

### 1. CI Pipeline (`ci.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches
- Called by CD pipeline (reusable workflow)

**Jobs:**
1. **Build** - Builds Docker image and shares across jobs
2. **Lint and Format** - Runs Black and Flake8 code quality checks
3. **Unit Tests** - Runs unit tests with 60% coverage threshold
4. **Integration Tests** - Tests API endpoint integration
5. **System Tests** - End-to-end tests with running server
6. **Test Summary** - Aggregates results and sends Slack notifications

**Coverage Requirements:**
- **Minimum**: 60% line coverage
- Coverage reports uploaded as artifacts

---

### 2. CD Pipeline (`cd.yml`)

**Triggers:**
- Push to `main` branch (automatic deployment)
- Manual workflow dispatch

**Jobs:**
1. **CI Tests** - Runs full CI pipeline first
2. **Build and Push** - Builds Docker images and pushes to Google Artifact Registry
3. **Deploy to Kubernetes** - Deploys to GKE cluster using Pulumi
4. **Post-Deployment Tests** - Runs smoke tests on deployed services
5. **Notification** - Reports deployment status via Slack

**Deployment Flow:**
```
Code merged to main
       ↓
Run CI tests (unit, integration, system)
       ↓
Build Docker images (API + Frontend)
       ↓
Push to Artifact Registry
       ↓
Deploy to GKE with Pulumi
       ↓
Run smoke tests
       ↓
Send notification
```

---

## Setup Instructions

### 1. Required GitHub Secrets

Go to: **Settings → Secrets and variables → Actions → New repository secret**

| Secret Name | Description | Required |
|-------------|-------------|----------|
| `GCP_KEY` | GCP service account JSON key | ✅ Yes |
| `PULUMI_ACCESS_TOKEN` | Pulumi access token for state management | ✅ Yes |
| `SLACK_WEBHOOK_URL` | Slack webhook for notifications | Optional |

### 2. Create GCP Service Account

```bash
# Set your project ID
PROJECT_ID="tummyai-ci-cd"

# Create service account
gcloud iam service-accounts create github-actions \
  --display-name="GitHub Actions CI/CD" \
  --project=$PROJECT_ID

SA_EMAIL="github-actions@${PROJECT_ID}.iam.gserviceaccount.com"

# Grant necessary roles
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SA_EMAIL" \
  --role="roles/container.developer"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SA_EMAIL" \
  --role="roles/artifactregistry.writer"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SA_EMAIL" \
  --role="roles/storage.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SA_EMAIL" \
  --role="roles/iam.serviceAccountUser"

# Create and download key
gcloud iam service-accounts keys create github-actions-key.json \
  --iam-account=$SA_EMAIL

# Copy contents to GitHub Secrets as GCP_KEY
cat github-actions-key.json

# Delete local key after adding to GitHub
rm github-actions-key.json
```

### 3. Get Pulumi Access Token

1. Go to [Pulumi Console](https://app.pulumi.com/)
2. Navigate to **Settings → Access Tokens**
3. Create a new token
4. Add to GitHub Secrets as `PULUMI_ACCESS_TOKEN`

---

## Local Testing

### Run CI Tests Locally

```bash
# Build Docker image
docker build -t tummyai-app-api:test src/api-service/

# Run unit tests with coverage
docker run --rm tummyai-app-api:test \
  pytest tests/unit/ -v --cov=api --cov-report=term

# Run integration tests
docker run --rm -e SKIP_DOWNLOAD=1 tummyai-app-api:test \
  pytest tests/integration/ -v

# Run system tests (requires running server)
docker run -d --name api-server -p 9000:9000 \
  -e DEV=1 tummyai-app-api:test
sleep 30
docker run --rm --network host tummyai-app-api:test \
  pytest tests/system/ -v
docker stop api-server && docker rm api-server
```

### Run Linting Locally

```bash
docker run --rm tummyai-app-api:test \
  black --check --line-length 120 api/

docker run --rm tummyai-app-api:test \
  flake8 --max-line-length=120 --extend-ignore=E203,W503 api/
```

---

## Deployment

### Manual Deployment

1. Go to GitHub repository → **Actions** tab
2. Select **"CD Pipeline - Deploy to Production"**
3. Click **"Run workflow"**
4. Select `main` branch
5. Click **"Run workflow"**

### Deploy with Pulumi Locally

```bash
cd src/deployment

# Deploy images
cd deploy_images
pulumi up

# Deploy Kubernetes resources
cd ../deploy_k8s
pulumi up
```

### Rollback Procedure

```bash
# Get GKE credentials
gcloud container clusters get-credentials tummyai-app-cluster \
  --zone=us-central1-a \
  --project=tummyai-ci-cd

# Rollback deployment
kubectl rollout undo deployment/api -n tummyai-app
kubectl rollout undo deployment/frontend -n tummyai-app

# Check status
kubectl rollout status deployment/api -n tummyai-app
kubectl rollout status deployment/frontend -n tummyai-app
```

---

## Monitoring

### View Workflow Runs

1. Go to repository **Actions** tab
2. Click on workflow run to see details
3. Expand jobs to see logs

### Monitor Kubernetes

```bash
# Get credentials
gcloud container clusters get-credentials tummyai-app-cluster \
  --zone=us-central1-a

# View pods
kubectl get pods -n tummyai-app

# View logs
kubectl logs -l run=api -n tummyai-app -f

# Check deployments
kubectl get deployments -n tummyai-app

# Check ingress
kubectl get ingress -n tummyai-app
```

---

## Troubleshooting

### CI Failures

| Issue | Solution |
|-------|----------|
| Docker build failed | Check `Dockerfile` in `src/api-service/` |
| Tests failed | Run tests locally first |
| Coverage too low | Add more unit tests (target: 60%) |
| Linting failed | Run `black` and `flake8` locally |

### CD Failures

| Issue | Solution |
|-------|----------|
| Authentication failed | Check `GCP_KEY` secret |
| Pulumi failed | Check `PULUMI_ACCESS_TOKEN` secret |
| Image push failed | Verify Artifact Registry permissions |
| Deployment timeout | Check pod logs in GKE |

---

## Pipeline Metrics

| Metric | Target |
|--------|--------|
| CI Build time | ~5-8 minutes |
| CI Test time | ~3-5 minutes |
| CD Deploy time | ~5-10 minutes |
| Total pipeline | ~15-20 minutes |
| Test coverage | ≥60% |

---

## Status Badges

Add to your README.md:

```markdown
![CI Pipeline](https://github.com/johnlin8427/tummyai-ci-cd/actions/workflows/ci.yml/badge.svg)
![CD Pipeline](https://github.com/johnlin8427/tummyai-ci-cd/actions/workflows/cd.yml/badge.svg)
```
