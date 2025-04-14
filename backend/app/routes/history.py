from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.services.s3_service import get_history
router = APIRouter()


@router.get("/historico", response_class=HTMLResponse)
def exibir_historico():
    get_history()
