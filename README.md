# AC215 - Milestone 5 - TummyAI

**Team Members**
- Nicole Ye (jiarong_ye@hms.harvard.edu)
- Ningxi Huang (ningxi_huang@hms.harvard.edu)
- John Lin (john_lin@hms.harvard.edu)
- Stephanie Chen (stephanie_chen@hms.harvard.edu)

## Project Overview

TummyAI is an AI-powered food recognition app designed to help individuals with irritable bowel syndrome (IBS) manage their digestive health. The application uses a fine-tuned Vision Transformer (ViT) model to identify 658 food dishes from images and provide ingredient-level FODMAP analysis across 707 ingredients. Users can upload meal photos, track symptoms, and receive personalized insights for their food triggers.

### Repository Organization

```
├── .github/workflows/      # CI/CD pipeline
├── src/                    # Source code
│   ├── api-service/        # APIs
│   ├── data-version/       # Data versioning
│   ├── deployment/         # App deployment
│   └── frontend-react/     # Frontend
├── docs/                   # Additional documentation
├── images/                 # Images
└── README.md               # This file
```

### Solution Architecture

![Mockup](images/solution_architecture.png)

### Technical Architecture

![Mockup](images/technical_architecture.png)

## Setup Instructions

### Prerequisites
- Install Docker
- Clone this repository
```bash
git clone https://github.com/Elococin/AC215_tummyai.git
```
- Setup up GCP credentials in a `secrets` directory

## Deployment Instructions

### APIs

1. Navigate to the `api-service` directory

```bash
cd src/api-service
```

2. Build and run the container.

```bash
sh docker-shell.sh
```

3. Start the API service.
```bash
uvicorn_server
```

4. View the API service at [http://localhost:9000](http://localhost:9000)

    You can also view an interactive API documentation at [http://localhost:9000/docs](http://localhost:9000/docs)

![Mockup](images/screenshot_api_service.png)

### Frontend

1. Navigate to the `frontend-react` directory.

```bash
cd src/frontend-react
```

2. Build and run the container.
```bash
sh docker-shell.sh
```

3. Install dependencies.
```bash
npm install
```

4. Start the development frontend server.
```
npm run dev
```

5. View the frontend at [http://localhost:3000](http://localhost:3000)

![Mockup](images/screenshot_frontend_react.png)

### Data Versioning

1. Navigate to the `data-version` directory.

```bash
cd src/data-version
```

2. Build and run the container.
```bash
sh docker-shell.sh
```

3. Inside the container, run:

```bash
dvc remote add -d gcs_data gs://tummyai-app-models/dvc_store
dvc pull
dvc add gcs_data
dvc push
```

4. Outside the container, run:

```bash
git status
git add .
git commit -m "DVC update"
git tag -a "dataset_v1" -m "tag dataset"
git push --atomic origin main dataset_v1
```

### Deployment

1. Navigate to the `deployment` directory.

```bash
cd src/deployment
```

2. Build and run the container.
```bash
sh docker-shell.sh
```

3. Build and push Docker images to Google Artifact Registry.

```bash
# Navigate to the `deploy_images` directory
cd deploy_images

# Set up Pulumi
pulumi stack init dev
pulumi config set gcp:project tummyai-ci-cd

# Build and push containers
pulumi up --stack dev --refresh -y
```

4. Deploy the application.

```bash
# Navigate to the `deploy_k8s` directory
cd deploy_k8s

# Set up Pulumi
pulumi stack init dev
pulumi config set gcp:project tummyai-ci-cd
pulumi config set security:gcp_service_account_email deployment@tummyai-ci-cd.iam.gserviceaccount.com --stack dev
pulumi config set security:gcp_ksa_service_account_email gcp-service@tummyai-ci-cd.iam.gserviceaccount.com --stack dev

# Create a Kubernetes cluster and deploy our containers
pulumi up --stack dev --refresh -y
```

## Usage Instructions

**URL:** [http://34.10.244.81.sslip.io/](http://34.10.244.81.sslip.io/)

### 🏠 Home Page

In the Home Page, users can upload a photo of their meal and report their symptoms. Our fine-tuned Vision Transformer model then analyzes the photo to identify the dish, ingredients, and overall FODMAP level.

![Mockup](images/screenshot_home.png)

### 📆 Meal History Page

In the Meal History Page, users can view their most recent meals and symptoms. Ingredients with high, low, or no FODMAP content are highlighted in red, yellow, and green, respectively.

![Mockup](images/screenshot_meal_history.png)

### ⓘ Health Report Page

In the Health Report Page, users can view trigger foods associated with their reported symptoms, as well as changes in these symptoms over time. In addition, our application uses Gemini to generate personalized recommendations based on user data.

![Mockup](images/screenshot_health_report.png)

### 🧀 Cheese Mode

Try turning on Cheese Mode in the top right corner!

![Mockup](images/screenshot_cheese_mode.png)

## Known Issues and Limitations

1. **Serverless ML Pipeline**

Due to the complexity of our ML pipeline, certain tasks (data collection, data processing, and model training) are performed manually. See the notebook for more details.

2. **Asynchronous User Input**

Currently, users are required to upload a meal photo and report their symptoms at the same time. In the future, we hope to allow users to report symptoms for previous meals in the Meal History Page.

3. **User Feedback**

At present, users are not able to edit the list of ingredients identified by our fine-tuned Vision Transformer model. We aim to implement this feature in both the Home and Meal History Pages.

## Additional Details (Technical Implementation)

### Kubernetes Deployment

Kubernetes demonstrates horizontal pod autoscaling behavior:

- Baseline: 2 pods
- Under load: Automatically scaled to 9 pods (memory at 132% of 80% target)
- Configuration: HPA monitors CPU (70% target) and memory (80% target)
- Range: 2-10 pods

**Autoscaling Behavior Demonstration:**

![Mockup](images/kubernetes.png)

### Pulumi Infrastructure

Pulumi automates the provisioning and deployment of our infrastructure and application.

**Provisioning and Deployment Demonstration:**

![Mockup](images/pulumi.png)

### CI Pipeline

Our Continuous Integration (CI) pipeline uses GitHub Actions to automate the following steps on push:

1. Build Docker image
2. Run linting and formatting checks
3. Run unit tests
4. Run integration tests
5. Run system tests

**CI Pipeline Workflow File:** `.github/workflows/ci.yml`

**CI Pipeline Screenshot**

![Mockup](images/ci_pipeline.png)

**CI Pipeline Coverage Report**

![Mockup](images/ci_pipeline_coverage.png)

**Functions/Modules Not Covered:** `docs/TEST_COVERAGE.md`

### CD Pipeline

Our Continuous Deployment (CD) pipeline extends the CI pipeline:

1. Build Docker image
2. Run linting and formatting checks
3. Run unit tests
4. Run integration tests
5. Run system tests
6. Build and push Docker images to Google Artifact Registry
7. Deploy application

**CD Pipeline Workflow File:** `.github/workflows/cd.yml`

**CD Pipeline Screenshot**

![Mockup](images/cd_pipeline.png)

![2afac60e4b3e4e2d84407452a97bfbd4](https://github.com/user-attachments/assets/682918ab-5227-4f92-8ffc-cb1f46b15576)

### ML Workflow
The workflow begins with the construction of a high-quality training dataset by harmonizing labels across multiple food image sources. We aim to combine Food-101 with MM-Food-100K and Vireo-172 dataset. Because the MM-Food-100K dataset contains over 15,000 heterogeneous and often noisy dish names, a GPT-based label harmonization pipeline was developed to align each label with the Food-101 taxonomy or produce a simplified, standardized label when no match existed. After harmonization, rare classes with fewer than 20 images were removed to ensure stable model training, resulting in a refined dataset of 67,654 images across 411 well-supported classes. Combineiung with Vireo-172 dataset, we ended up with 180K+ images of 658 dishes, and we split them into test train sets.

Ingredient datasets were mainly harmonized from the ingredients lists from MM-Food-100K dataset. For Chinese cuisines from VIREO Food-172, GPT API was prompted as an expert chef to expand on missing ingredients and normalize synonyms (i.e. scallions and green onions), generating a granular, harmonized ingredient list. FODMAP data dictionaries were created using a multi-step harmonization pipeline. To extend the interpretability and dietary relevance of the constructed ingredient database, each ingredient was annotated with a corresponding FODMAP level (Low, Medium, or High). Existing resources, such as Monash University’s laboratory-tested lists, do not cover the full ingredient vocabulary that emerged from the merged MM-Food-100K + VIREO Food-172 + GPT-generated ingredient set [5]. We therefore designed a hybrid annotation pipeline using both rule-based matching and GPT-augmented classification. FODMAP categorization enables downstream applications such as IBS-friendly meal recommendation, medical nutrition analysis, and sensitivity-aware food classification.

Press enter or click to view image in full size


| Step  | Training Loss | Validation Loss | Accuracy | Top-5 Accuracy |
| ----- | ------------- | --------------- | -------- | -------------- |
| 500   | 5.718600      | 5.674112        | 0.092340 | 0.291022       |
| 1000  | 5.076100      | 5.083273        | 0.250774 | 0.515693       |
| 1500  | 4.594600      | 4.573081        | 0.332036 | 0.617349       |
| 2000  | 4.139300      | 4.124670        | 0.400829 | 0.676314       |
| 2500  | 3.824500      | 3.740117        | 0.456244 | 0.720027       |
| 3000  | 3.468900      | 3.414407        | 0.497373 | 0.743659       |
| 3500  | 3.141000      | 3.127199        | 0.529099 | 0.766836       |
| 4000  | 2.918600      | 2.892709        | 0.557474 | 0.778283       |
| 4500  | 2.555700      | 2.677940        | 0.585736 | 0.794103       |
| 5000  | 2.377500      | 2.499819        | 0.603772 | 0.807055       |
| 5500  | 2.223700      | 2.354410        | 0.618939 | 0.816343       |
| 6000  | 2.212300      | 2.235670        | 0.632005 | 0.821882       |
| 6500  | 2.021500      | 2.127721        | 0.642855 | 0.829949       |
| 7000  | 1.985000      | 2.036654        | 0.652171 | 0.834124       |
| 7500  | 1.864000      | 1.959209        | 0.662482 | 0.839208       |
| 8000  | 1.797800      | 1.896871        | 0.668787 | 0.843554       |
| 8500  | 1.753000      | 1.839163        | 0.675462 | 0.846962       |
| 9000  | 1.576200      | 1.792664        | 0.680461 | 0.852132       |
| 9500  | 1.587500      | 1.747615        | 0.683586 | 0.853495       |
| 10000 | 1.494400      | 1.715904        | 0.685432 | 0.853495       |
| 10500 | 1.495600      | 1.693280        | 0.688215 | 0.856108       |
| 11000 | 1.407700      | 1.663654        | 0.692135 | 0.857557       |
| 11500 | 1.366000      | 1.644924        | 0.694464 | 0.859062       |
| 12000 | 1.388300      | 1.631460        | 0.697305 | 0.859602       |
| 12500 | 1.434300      | 1.622274        | 0.698696 | 0.859801       |
| 13000 | 1.429600      | 1.617304        | 0.698100 | 0.860624       |


TrainOutput(global_step=13188,
            training_loss=2.5605,
            metrics={
                'train_runtime': 4641.5937,
                'train_samples_per_second': 90.902,
                'train_steps_per_second': 2.841,
                'total_flos': 3.29e+19,
                'train_loss': 2.5605,
                'epoch': 3.0})


Overall, the model shows consistent improvement throughout training, with validation loss steadily decreasing and top-1 accuracy rising from 9% to nearly 70%. Top-5 accuracy exceeds 86% by step 13,000, indicating that the fine-tuned model successfully learns the expanded food label space derived from the harmonized dataset.




