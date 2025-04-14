from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from app.services.s3_service import upload_file_to_s3
from app.core.utils import registrar_acao

router = APIRouter()

@router.post("/")
async def upload_csv(file: UploadFile = File(...), user: str = Form(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Apenas arquivos .csv são permitidos.")
    url = await upload_file_to_s3(file)
    registrar_acao(user, "file_upload", "success", file.filename)
    return {"message": "Upload realizado com sucesso", "url": url}
