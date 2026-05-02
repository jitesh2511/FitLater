from fitlater.config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE_MB, MAX_COLS, MAX_ROWS

import uuid
import os
import tempfile
import pandas as pd

def clean_types(obj):
    import numpy as np
    import math

    if isinstance(obj, dict):
        return {k: clean_types(v) for k, v in obj.items()}

    elif isinstance(obj, list):
        return [clean_types(v) for v in obj]

    elif isinstance(obj, np.integer):
        return int(obj)

    elif isinstance(obj, np.floating):
        val = float(obj)
        if math.isnan(val) or math.isinf(val):
            return None
        return val

    elif isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
        return obj

    else:
        return obj

def is_valid_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def is_file_size_valid(file) -> bool:
    file.file.seek(0, 2)  # move to end
    size = file.file.tell()
    file.file.seek(0)     # reset pointer

    return size <= MAX_FILE_SIZE_MB * 1024 * 1024


# Keep transient uploads out of the project tree to avoid dev-server auto reloads.
UPLOAD_DIR = os.path.join(tempfile.gettempdir(), "fitlater_uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_temp_file(file):
    unique_name = f"{uuid.uuid4()}.csv"
    file_path = os.path.join(UPLOAD_DIR, unique_name)

    # Explicitly seek to start before reading
    file.file.seek(0)
    
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return file_path

def load_csv_safe(path):
    try:
        df = pd.read_csv(path)
        if df.empty:
            raise ValueError("Empty dataset")
        return df
    except Exception:
        raise ValueError("Invalid or corrupted CSV file")

def cleanup_file(path):
    if os.path.exists(path):
        os.remove(path)
    
def validate_dataset(df):
    if df is None:
        raise ValueError("Dataset could not be loaded")

    if df.empty:
        raise ValueError("Dataset is empty")

    if df.shape[0] < 2:
        raise ValueError("Dataset must have at least 2 rows")

    if df.shape[1] < 1:
        raise ValueError("Dataset must have at least 1 column")
    
    if df.shape[0] > MAX_ROWS:
        raise ValueError(f"Dataset too large (max {MAX_ROWS} rows allowed)")
    
    if df.shape[1] > MAX_COLS:
        raise ValueError(f"Dataset too large (max {MAX_COLS} columns allowed)")