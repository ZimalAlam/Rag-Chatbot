from fastapi import APIRouter, UploadFile, File
import shutil, os
from app.sql_agent.database import DatabaseManager
from app.core.config import CSV_UPLOAD_DIR

router = APIRouter()

@router.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    file_path = os.path.join(CSV_UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    table_name = os.path.splitext(file.filename)[0]
    db = DatabaseManager()
    db.upload_csv_to_db(file_path, table_name)

    return {"message": f"Stored as table {table_name}"}
