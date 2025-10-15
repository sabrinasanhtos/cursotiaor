from app.crud.maquinas import listar_maquinas, cadastrar_maquina, editar_maquina, excluir_maquina
from app.models.maquinas import MaquinaCreate, MaquinaUpdate
from fastapi import HTTPException

def obter_maquinas():
    maquinas = listar_maquinas()
    if not maquinas:
        return []
    return maquinas

def criar_maquina(data: MaquinaCreate):
    try:
        return cadastrar_maquina(data.modelo, data.tipo, data.ano_fabricacao, data.status)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao cadastrar máquina: {e}")

def atualizar_maquina(maquina_id: int, data: MaquinaUpdate):
    try:
        return editar_maquina(maquina_id, data.modelo, data.tipo, data.ano_fabricacao, data.status)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar máquina: {e}")

def remover_maquina(maquina_id: int):
    try:
        return excluir_maquina(maquina_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao excluir máquina: {e}")