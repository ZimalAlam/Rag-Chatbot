import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "data")

PDF_UPLOAD_DIR = os.path.join(DATA_DIR, "pdf_uploads")
EXTRACTED_DIR = os.path.join(DATA_DIR, "extracted")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
CHUNKED_DIR = os.path.join(DATA_DIR, "chunks")
VECTOR_DIR = os.path.join(DATA_DIR, "vectors")
CSV_UPLOAD_DIR = os.path.join(DATA_DIR, "csv_uploads")

for path in [
    PDF_UPLOAD_DIR,
    EXTRACTED_DIR,
    PROCESSED_DIR,
    CHUNKED_DIR,
    VECTOR_DIR,
    CSV_UPLOAD_DIR
]:
    os.makedirs(path, exist_ok=True)
