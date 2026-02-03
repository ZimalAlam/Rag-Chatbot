from fastapi import APIRouter, UploadFile, File
import shutil, os

from app.core.config import PDF_UPLOAD_DIR, EXTRACTED_DIR, PROCESSED_DIR, CHUNKED_DIR, VECTOR_DIR
from app.rag_agent.pdf_extractor import extract_pdfs
from app.rag_agent.preprocessor import preprocess_extracted_text
from app.rag_agent.chunker import chunk_processed_texts
from app.rag_agent.embedder import load_chunks, build_faiss_index, save_index
from sentence_transformers import SentenceTransformer

router = APIRouter()

@router.post("/upload-pdf/")
async def upload_pdf(files: list[UploadFile] = File(...)):
    for file in files:
        file_path = os.path.join(PDF_UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    extract_pdfs(PDF_UPLOAD_DIR, EXTRACTED_DIR)
    preprocess_extracted_text(EXTRACTED_DIR, PROCESSED_DIR)
    chunk_processed_texts(PROCESSED_DIR, CHUNKED_DIR)

    model = SentenceTransformer("all-MiniLM-L6-v2")
    texts, metadata = load_chunks(CHUNKED_DIR)
    index = build_faiss_index(texts, model)
    save_index(index, metadata, VECTOR_DIR)

    return {"message": "PDFs processed."}
