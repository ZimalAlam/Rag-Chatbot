from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes_pdf import router as pdf_router
from app.api.routes_csv import router as csv_router
from app.api.routes_chat import router as chat_router

app = FastAPI(title="Agentic AI System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pdf_router)
app.include_router(csv_router)
app.include_router(chat_router)
