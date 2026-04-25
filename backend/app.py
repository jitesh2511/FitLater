from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io
from backend.engine import get_result

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

    if not file.filename.endswith(".csv"):
        return {"error": "Only CSV files are supported"}

    content = await file.read()

    try:
        df = pd.read_csv(io.BytesIO(content))
    except Exception:
        return {"error": "Invalid CSV file"}

    return get_result(df)