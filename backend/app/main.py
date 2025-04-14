from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import upload, create_table, history


app = FastAPI(title="Backend API - Upload CSV")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # para aceitar requisições do Streamlit
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrando as rotas
app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(create_table.router, prefix="/athena", tags=["Athena"])
app.include_router(history.router, prefix="/history", tags=["History"])

