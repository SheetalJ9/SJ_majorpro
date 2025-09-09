from pathlib import Path
import os

# Get the project root (assuming config.py is in src/ folder)
# This goes up from src/ to project root
PROJECT_ROOT = Path(__file__).parent.parent
# Alternative: PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Data paths
DATA_DIR = PROJECT_ROOT / 'data'
SQL_LITE_FILE_NAME = DATA_DIR / 'raw' / 'tpcds.db'
PROCESSED_DATA_FILE = DATA_DIR / 'processed' / 'processed.csv'

# Model paths
MODELS_DIR = PROJECT_ROOT / 'models'
LATEST_MODEL_FILE = MODELS_DIR / 'latest' / 'final_model.pkl'
BEST_PARAMS_FILE = MODELS_DIR / 'best_params.pkl'
PREPROCESSOR_OBJ_FILE = MODELS_DIR / 'preprocessor.pkl'
MODEL_VERSIONS_FOLDER = MODELS_DIR / 'versioned_models'

# MLflow
MLFLOW_TRACKING_URI = "mlruns"


# Create directories if they don't exist
def ensure_directories():
    """Create necessary directories if they don't exist"""
    directories = [
        DATA_DIR / 'raw',
        DATA_DIR / 'processed',
        MODELS_DIR / 'latest',
        MODELS_DIR,
        MODEL_VERSIONS_FOLDER
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


# Debug information
if __name__ == "__main__":
    print("Project structure:")
    print(f"PROJECT_ROOT: {PROJECT_ROOT.resolve()}")
    print(f"SQL_LITE_FILE_NAME: {SQL_LITE_FILE_NAME.resolve()}")
    print(f"Database exists: {SQL_LITE_FILE_NAME.exists()}")

    if not SQL_LITE_FILE_NAME.exists():
        print("\nLooking for database files in project:")
        for db_file in PROJECT_ROOT.rglob("*.db"):
            print(f"  Found: {db_file}")