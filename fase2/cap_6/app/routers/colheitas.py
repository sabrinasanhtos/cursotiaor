from fastapi import APIRouter
from app.services.colheitas import criar_colheita, encerrar_colheita, obter_colheitas
from app.models.colheitas import ColheitaCreate

router = APIRouter(prefix="/colheitas", tags=["Colheitas"])

@router.post("/iniciar")
def iniciar_colheita(data: ColheitaCreate):
    return criar_colheita(data.maquina_id)

@router.put("/finalizar/{colheita_id}")
def finalizar_colheita(colheita_id: int):
    return encerrar_colheita(colheita_id)

@router.get("/listar")
def listar_colheitas():
    """Lista todas as colheitas registradas com suas respectivas máquinas."""
    return obter_colheitas()