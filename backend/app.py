from fastapi import FastAPI, UploadFile, HTTPException, File
from fastapi.middleware.cors import CORSMiddleware
import io
from backend.engine import get_result
from backend.util import is_valid_file, is_file_size_valid, save_temp_file, cleanup_file, load_csv_safe, validate_dataset

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "FitLater API is running"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    if not is_valid_file(file.filename):
        raise HTTPException(status_code=400, detail="Only CSV files allowed")

    if not is_file_size_valid(file):
        raise HTTPException(status_code=400, detail="File too large")

    file_path = save_temp_file(file)

    try:
        df = load_csv_safe(file_path)

        validate_dataset(df)

        result = get_result(df)

        return result

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    finally:
        cleanup_file(file_path)