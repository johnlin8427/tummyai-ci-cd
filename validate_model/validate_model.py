import csv
import os
import sys
from pathlib import Path
import torch
from PIL import Image
from transformers import AutoImageProcessor, AutoModelForImageClassification
from tqdm import tqdm
from google.cloud import storage

# Paths
SCRIPT_DIR = Path(__file__).parent
CSV_PATH = SCRIPT_DIR / "test_labels.csv"
MODEL_LOCAL_PATH = "/tmp/validate_model"
MODEL_GCS_PATH = "models/v2"  # Adjust to match your model path in GCS

def download_model_from_gcs():
    """Download model from GCS bucket."""
    gcs_bucket_name = os.getenv("GCS_BUCKET_NAME")
    if not gcs_bucket_name:
        raise ValueError("GCS_BUCKET_NAME environment variable not set")

    model_dir = Path(MODEL_LOCAL_PATH)
    model_dir.mkdir(parents=True, exist_ok=True)

    model_files = ["config.json", "preprocessor_config.json", "model.safetensors"]

    print(f"⬇️  Downloading model from gs://{gcs_bucket_name}/{MODEL_GCS_PATH}")

    try:
        client = storage.Client()
        bucket = client.bucket(gcs_bucket_name)

        for filename in model_files:
            gcs_path = f"{MODEL_GCS_PATH}/{filename}"
            local_path = model_dir / filename

            if local_path.exists():
                print(f"   ✓ {filename} already exists locally")
                continue

            print(f"   ⬇️  Downloading {filename}...", end=" ")
            blob = bucket.blob(gcs_path)
            blob.download_to_filename(str(local_path))
            print("✓")

        print(f"✅ Model downloaded to {MODEL_LOCAL_PATH}")

    except Exception as e:
        print(f"❌ Error downloading model from GCS: {e}")
        raise


def verify_model_files():
    """Check if all required model files exist locally."""
    required_files = ["config.json", "model.safetensors"]
    model_dir = Path(MODEL_LOCAL_PATH)

    for filename in required_files:
        if not (model_dir / filename).exists():
            return False
    return True


def load_model():
    """Load model from local path, downloading from GCS if needed."""
    # Download model if not present locally
    if not verify_model_files():
        print("Model not found locally, downloading from GCS...")
        download_model_from_gcs()

    if not verify_model_files():
        raise FileNotFoundError(f"Model files not found at {MODEL_LOCAL_PATH}")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    processor = AutoImageProcessor.from_pretrained(MODEL_LOCAL_PATH)
    model = AutoModelForImageClassification.from_pretrained(MODEL_LOCAL_PATH)
    model.to(device)
    model.eval()

    return processor, model, device


def predict(image_path, processor, model, device):
    img = Image.open(image_path).convert("RGB")
    inputs = processor(images=img, return_tensors="pt").to(device)

    with torch.no_grad():
        logits = model(**inputs).logits
        probs = torch.softmax(logits, dim=-1)

    top_probs, top_idx = torch.topk(probs, 5)

    result = []
    for prob, idx in zip(top_probs[0], top_idx[0]):
        label = model.config.id2label[idx.item()]
        result.append((label, float(prob)))

    return result


def main():
    processor, model, device = load_model()

    top1 = 0
    top5 = 0
    total = 0

    # Read test labels
    with open(CSV_PATH, "r") as f:
        reader = csv.reader(f)
        next(reader)  # skip header

        for img_path, true_label in tqdm(reader, desc="Validating"):
            # Convert relative path to absolute path
            full_img_path = SCRIPT_DIR / img_path
            preds = predict(full_img_path, processor, model, device)
            
            pred_top1 = preds[0][0].lower()
            pred_top5 = [p[0].lower() for p in preds]

            true = true_label.lower()

            if pred_top1 == true:
                top1 += 1

            if true in pred_top5:
                top5 += 1

            total += 1

            # Print results image-by-image
            print(f"\nImage: {img_path}")
            print(f"True label: {true_label}")
            print("Top-5 predictions:")
            for label, prob in preds:
                print(f"  {label:25s}  {prob:.4f}")

    print("\n==== FINAL RESULTS ====")
    print(f"Total images: {total}")
    print(f"Top-1 accuracy: {top1/total*100:.2f}%")
    print(f"Top-5 accuracy: {top5/total*100:.2f}%")

if __name__ == "__main__":
    main()
