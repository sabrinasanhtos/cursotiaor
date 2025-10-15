import math
from app.core.database import get_connection

# ---------------------------------------------
# Funções de CRUD e Cálculos de Colheita
# ---------------------------------------------

def iniciar_colheita(maquina_id: int):
    """Cria uma nova colheita e retorna o ID gerado."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                colheita_id = cursor.var(int)
                cursor.execute("""
                    INSERT INTO colheitas (maquina_id, inicio, status)
                    VALUES (:1, SYSTIMESTAMP, 'Em andamento')
                    RETURNING id INTO :2
                """, (maquina_id, colheita_id))
                conn.commit()
                new_id = colheita_id.getvalue()[0]
                print(f"✅ Colheita iniciada (ID: {new_id})")
                return new_id
    except Exception as e:
        raise RuntimeError(f"Erro ao iniciar colheita: {e}")


def inserir_ponto(colheita_id: int, lat: float, lon: float):
    """Insere um novo ponto GPS no trajeto da colheita."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO pontos_trajeto (colheita_id, latitude, longitude)
                    VALUES (:1, :2, :3)
                """, (colheita_id, lat, lon))
                conn.commit()
                print(f"📍 Ponto registrado (Colheita {colheita_id}): {lat}, {lon}")
    except Exception as e:
        raise RuntimeError(f"Erro ao inserir ponto de trajeto: {e}")


def _calcular_distancia(lat1, lon1, lat2, lon2):
    """Calcula a distância entre dois pontos GPS (Haversine) em metros."""
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def finalizar_colheita(colheita_id: int):
    """Finaliza a colheita, calcula distância total, área e duração."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # Buscar os pontos
                cursor.execute("""
                    SELECT latitude, longitude
                    FROM pontos_trajeto
                    WHERE colheita_id = :1
                    ORDER BY id
                """, (colheita_id,))
                pontos = cursor.fetchall()

                area_colhida = 0.0
                if pontos and len(pontos) > 1:
                    distancia_total = 0.0
                    for i in range(1, len(pontos)):
                        try:
                            lat1, lon1 = float(pontos[i-1][0]), float(pontos[i-1][1])
                            lat2, lon2 = float(pontos[i][0]), float(pontos[i][1])
                            if (lat1, lon1) != (lat2, lon2):
                                distancia_total += _calcular_distancia(lat1, lon1, lat2, lon2)
                        except Exception:
                            continue

                    # largura média de 5m para conversão em hectares
                    area_colhida = round((distancia_total * 5) / 10000, 2)

                # Atualiza colheita
                cursor.execute("""
                    UPDATE colheitas
                    SET fim = SYSTIMESTAMP,
                        status = 'Concluída',
                        area_colhida = :1,
                        duracao = ROUND((CAST(SYSTIMESTAMP AS DATE) - CAST(inicio AS DATE)) * 24, 2)
                    WHERE id = :2
                """, (area_colhida, colheita_id))
                conn.commit()

                if cursor.rowcount == 0:
                    print(f"⚠️ Nenhuma colheita encontrada com ID {colheita_id}")
                    raise RuntimeError(f"Nenhuma colheita atualizada (id={colheita_id})")

                print(f"✅ Colheita {colheita_id} concluída — Área: {area_colhida} ha")

        return {"colheita_id": colheita_id, "status": "Concluída", "area_colhida": area_colhida}

    except Exception as e:
        raise RuntimeError(f"Erro ao finalizar colheita: {e}")

def listar_colheitas():
    """Lista todas as colheitas com dados da máquina associada."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        c.id,
                        c.maquina_id,
                        m.modelo,
                        m.tipo,
                        m.ano_fabricacao,
                        c.inicio,
                        c.fim,
                        c.status,
                        NVL(c.area_colhida, 0),
                        NVL(c.duracao, 0)
                    FROM colheitas c
                    JOIN maquinas m ON m.id = c.maquina_id
                    ORDER BY c.id DESC
                """)
                registros = cursor.fetchall()

                return [
                    {
                        "id": row[0],
                        "maquina_id": row[1],
                        "modelo": row[2],
                        "tipo": row[3],
                        "ano_fabricacao": row[4],
                        "inicio": row[5],
                        "fim": row[6],
                        "status": row[7],
                        "area_colhida": float(row[8]),
                        "duracao_horas": _formatar_duracao(row[9])
                    }
                    for row in registros
                ]
    except Exception as e:
        raise RuntimeError(f"Erro ao listar colheitas: {e}")
    
def _formatar_duracao(valor):
    """Converte horas decimais (ex: 0.03 → '2 min', 1.5 → '1h 30min')."""
    if valor is None:
        return "-"
    try:
        total_min = round(float(valor) * 60)
        if total_min < 1:
            return "< 1 min"
        horas = total_min // 60
        minutos = total_min % 60
        if horas == 0:
            return f"{minutos} min"
        if minutos == 0:
            return f"{horas}h"
        return f"{horas}h {minutos}min"
    except Exception:
        return "-"