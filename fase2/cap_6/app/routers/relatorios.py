from fastapi import APIRouter, Query
from app.services.relatorios import analisar_trafego

router = APIRouter(prefix="/relatorios", tags=["Relatórios"])

@router.get("/trafego")
def relatorio_trafego(colheita_id: int = Query(...)):
    return analisar_trafego(colheita_id)
