import time, random, threading
from app.crud.colheitas import iniciar_colheita, finalizar_colheita, inserir_ponto, listar_colheitas
from fastapi import HTTPException

# Dicionário para controlar colheitas em andamento
_colheitas_ativas = {}

# ---------------------------------------------
# Simulação de coleta em background
# ---------------------------------------------
def _simular_coleta(colheita_id: int):
    """Simula inserção contínua de coordenadas GPS enquanto a colheita está ativa."""
    print(f"🚜 Iniciando coleta de pontos para colheita {colheita_id}")
    while _colheitas_ativas.get(colheita_id, False):
        lat = -21.523 + random.uniform(-0.0005, 0.0005)
        lon = -47.826 + random.uniform(-0.0005, 0.0005)
        inserir_ponto(colheita_id, lat, lon)
        time.sleep(5)
    print(f"✅ Colheita {colheita_id} finalizada — coleta encerrada.")


# ---------------------------------------------
# Criar e Encerrar colheita
# ---------------------------------------------
def criar_colheita(maquina_id: int):
    """Inicia uma nova colheita e começa a coleta simulada de coordenadas."""
    try:
        colheita_id = iniciar_colheita(maquina_id)
        _colheitas_ativas[colheita_id] = True
        thread = threading.Thread(target=_simular_coleta, args=(colheita_id,), daemon=True)
        thread.start()
        return {"colheita_id": colheita_id, "status": "Em andamento"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao iniciar colheita: {e}")


def encerrar_colheita(colheita_id: int):
    """Finaliza a colheita, encerra a coleta e calcula área/duração."""
    try:
        _colheitas_ativas[colheita_id] = False
        finalizar_colheita(colheita_id)
        return {"colheita_id": colheita_id, "status": "Concluída"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao finalizar colheita: {e}")


# ---------------------------------------------
# NOVO: Listar colheitas
# ---------------------------------------------
def obter_colheitas():
    """Retorna todas as colheitas registradas no banco."""
    try:
        colheitas = listar_colheitas()
        if not colheitas:
            return {"mensagem": "Nenhuma colheita registrada ainda."}
        return colheitas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar colheitas: {e}")