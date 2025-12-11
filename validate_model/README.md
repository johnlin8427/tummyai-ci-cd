# Model Validation Script

This script validates the TummyAI food classification model by running predictions on a test dataset and calculating Top-1 and Top-5 accuracy metrics.

## Setup

1. **Install dependencies**:
   ```bash
   cd validate_model
   pip install -r requirements.txt
   ```

2. **Set environment variables**:
   ```bash
   export GCS_BUCKET_NAME="your-gcs-bucket-name"
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"
   ```

3. **Verify test data**:
   - `test_labels.csv` contains image paths and ground truth labels
   - `test_images/` contains the actual test images

## Usage

Run the validation script:

```bash
python validate_model.py
```

The script will:
1. Check if the model exists locally at `/tmp/validate_model`
2. If not found, download the model from GCS bucket at `models/v2`
3. Load the model and run predictions on all test images
4. Display predictions for each image
5. Calculate and display final Top-1 and Top-5 accuracy

## Configuration

You can adjust the model path in the script by changing:
```python
MODEL_GCS_PATH = "models/v2"  # Path to model in GCS bucket
MODEL_LOCAL_PATH = "/tmp/validate_model"  # Local cache location
```

## Output

The script provides:
- **Per-image output**: Shows the true label and top-5 predictions with confidence scores
- **Final metrics**:
  - Top-1 Accuracy: % of images where the top prediction matches the true label
  - Top-5 Accuracy: % of images where the true label appears in the top-5 predictions

## Example Output

```
⬇️  Downloading model from gs://your-bucket/models/v2
   ⬇️  Downloading config.json... ✓
   ⬇️  Downloading preprocessor_config.json... ✓
   ⬇️  Downloading model.safetensors... ✓
✅ Model downloaded to /tmp/validate_model
Using device: cpu

Image: test_images/sample_0_mussels.jpg
True label: mussels
Top-5 predictions:
  mussels                    0.9234
  clam chowder               0.0456
  oysters                    0.0123
  ...

==== FINAL RESULTS ====
Total images: 7
Top-1 accuracy: 85.71%
Top-5 accuracy: 100.00%
```
