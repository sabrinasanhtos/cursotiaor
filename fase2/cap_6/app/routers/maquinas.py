from fastapi import APIRouter
from app.models.maquinas import MaquinaCreate, MaquinaUpdate
from app.services.maquinas import obter_maquinas, criar_maquina, atualizar_maquina, remover_maquina

router = APIRouter(prefix="/maquinas", tags=["Máquinas"])

@router.get("/listar")
def listar_maquinas():
    """Retorna todas as máquinas cadastradas."""
    return obter_maquinas()

@router.post("/cadastrar")
def cadastrar_maquina(data: MaquinaCreate):
    """Cadastra uma nova máquina."""
    return criar_maquina(data)

@router.put("/editar/{maquina_id}")
def editar_maquina(maquina_id: int, data: MaquinaUpdate):
    """Edita uma máquina existente."""
    return atualizar_maquina(maquina_id, data)

@router.delete("/excluir/{maquina_id}")
def excluir_maquina(maquina_id: int):
    """Exclui uma máquina existente."""
    return remover_maquina(maquina_id)