from fastapi import HTTPException
import oracledb
from app.core.database import get_connection

from fastapi import HTTPException
from app.core.database import get_connection
import oracledb

def listar_maquinas():
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT id, modelo, tipo, ano_fabricacao, status
                    FROM maquinas
                    ORDER BY id
                """)
                rows = cursor.fetchall()
                return [
                    {
                        "id": r[0],
                        "modelo": r[1],
                        "tipo": r[2],
                        "ano_fabricacao": r[3],
                        "status": bool(r[4])
                    } for r in rows
                ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar máquinas: {e}")

def cadastrar_maquina(modelo: str, tipo: str, ano_fabricacao: int = None, status: bool = True):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                output_id = cursor.var(int)
                cursor.execute("""
                    INSERT INTO maquinas (modelo, tipo, ano_fabricacao, status)
                    VALUES (:1, :2, :3, :4)
                    RETURNING id INTO :5
                """, (modelo, tipo, ano_fabricacao, int(status), output_id))
                conn.commit()
                novo_id = output_id.getvalue()
                return {"id": novo_id, "mensagem": "Máquina cadastrada com sucesso!"}
    except oracledb.IntegrityError as e:
        raise HTTPException(status_code=400, detail=f"Violação de integridade: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao cadastrar máquina: {e}")

def editar_maquina(maquina_id: int, modelo: str, tipo: str, ano_fabricacao: int = None, status: bool = True):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE maquinas
                    SET modelo = :1,
                        tipo = :2,
                        ano_fabricacao = :3,
                        status = :4
                    WHERE id = :5
                """, (modelo, tipo, ano_fabricacao, int(status), maquina_id))
                conn.commit()

                if cursor.rowcount == 0:
                    raise HTTPException(status_code=404, detail=f"Máquina {maquina_id} não encontrada.")
                return {"mensagem": f"Máquina {maquina_id} atualizada com sucesso."}
    except oracledb.IntegrityError as e:
        raise HTTPException(status_code=400, detail=f"Erro de integridade: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar máquina: {e}")

def excluir_maquina(maquina_id: int):
    """Exclui uma máquina, com tratamento de integridade referencial."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM maquinas WHERE id = :1", [maquina_id])
                conn.commit()

                if cursor.rowcount == 0:
                    raise HTTPException(status_code=404, detail=f"Máquina {maquina_id} não encontrada.")
                return {"mensagem": "Máquina excluída com sucesso!"}
    except oracledb.IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Esta máquina está vinculada a colheitas e não pode ser excluída."
        )
    except oracledb.DatabaseError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco Oracle: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao excluir máquina: {e}")
