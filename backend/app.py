'''
FastAPI application for the FitLater backend API.

- Exposes endpoints for health check (`/`) and file upload (`/upload`)
- Handles dataset upload, validation, and invokes the main processing pipeline
- Configures CORS for integration with the frontend
- Handles validation and errors for file uploads

See README for usage instructions.
'''


from fastapi import FastAPI, UploadFile, HTTPException, File
from fastapi.middleware.cors import CORSMiddleware
from backend.engine import get_result
from backend.util import is_valid_file, is_file_size_valid, save_temp_file, cleanup_file, load_csv_safe, validate_dataset

from fitlater.logger.logger_instance import logger

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict later
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "FitLater API is running"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    logger.info(f'Received file: {file.filename}')

    if not is_valid_file(file.filename):
        logger.warning("Invalid file type uploaded")
        raise HTTPException(status_code=400, detail="Only CSV files allowed")

    if not is_file_size_valid(file):
        logger.warning("File size too large")
        raise HTTPException(status_code=400, detail="File too large")

    file_path = None

    try:

        file_path = save_temp_file(file)
        logger.info(f'File saved at {file_path}')

        df = load_csv_safe(file_path)
        logger.info(f'Dataset loaded: {df.shape}')

        validate_dataset(df)

        result = get_result(df)
        logger.info("Processing completed successfully")

        return result

    except ValueError as e:
        logger.exception(f'Error processing file: {str(e)}')
        raise HTTPException(status_code=400, detail="Invalid dataset")

    finally:
        cleanup_file(file_path)
        logger.info(f"Cleaned up file: {file_path}")
        

@app.post("/log-error")
async def log_error(payload: dict):
    logger.error(f"Frontend Error: {payload}")
    return {"status": "logged"}