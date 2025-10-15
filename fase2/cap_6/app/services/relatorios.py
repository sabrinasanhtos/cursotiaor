from app.core.database import get_connection
import math, os, folium

def _calcular_distancia(lat1, lon1, lat2, lon2):
    """Calcula a distância entre dois pontos GPS (Haversine) em metros."""
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def _buscar_pontos(colheita_id: int):
    """Busca pontos GPS da colheita informada."""
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT latitude, longitude
                FROM pontos_trajeto
                WHERE colheita_id = :1
                ORDER BY id
            """, (colheita_id,))
            return [{"lat": row[0], "lon": row[1]} for row in cursor.fetchall()]


def _buscar_dados_colheita(colheita_id: int):
    """Busca dados da colheita e da máquina associada."""
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT c.id, c.maquina_id, c.inicio, c.fim, c.status,
                       m.modelo, m.tipo, m.ano_fabricacao
                FROM colheitas c
                JOIN maquinas m ON m.id = c.maquina_id
                WHERE c.id = :1
            """, (colheita_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return {
                "colheita_id": row[0],
                "maquina_id": row[1],
                "inicio": str(row[2]) if row[2] else None,
                "fim": str(row[3]) if row[3] else None,
                "status": row[4],
                "maquina": {
                    "modelo": row[5],
                    "tipo": row[6],
                    "ano_fabricacao": row[7]
                }
            }


def _buscar_outras_maquinas(colheita_id: int):
    """Busca pontos de outras máquinas concluídas."""
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT p.latitude, p.longitude, c.maquina_id
                FROM pontos_trajeto p
                JOIN colheitas c ON c.id = p.colheita_id
                WHERE c.id <> :1 AND c.status = 'Concluída'
            """, (colheita_id,))
            return [{"lat": row[0], "lon": row[1], "maquina_id": row[2]} for row in cursor.fetchall()]


def _gerar_mapa_trafego(colheita_id, colheita, pontos, sobreposicoes):
    """Gera um mapa HTML mostrando rota e sobreposições."""
    if not pontos:
        return None

    os.makedirs("app/static/maps", exist_ok=True)
    mapa_path = f"app/static/maps/mapa_colheita_{colheita_id}.html"

    lat_centro = sum(p["lat"] for p in pontos) / len(pontos)
    lon_centro = sum(p["lon"] for p in pontos) / len(pontos)
    mapa = folium.Map(location=[lat_centro, lon_centro], zoom_start=16)

    # rota principal (verde)
    folium.PolyLine(
        [(p["lat"], p["lon"]) for p in pontos],
        color="green", weight=4,
        tooltip=f"Colheita {colheita_id} - {colheita['maquina']['modelo']}"
    ).add_to(mapa)

    # pontos sobrepostos (vermelho)
    for s in sobreposicoes:
        folium.CircleMarker(
            location=[s["lat"], s["lon"]],
            radius=4, color="red", fill=True,
            tooltip=f"Sobreposição com máquina {s['outra_maquina']}"
        ).add_to(mapa)

    mapa.save(mapa_path)
    return mapa_path


def analisar_trafego(colheita_id: int):
    """Analisa uma colheita específica e retorna informações de trajeto e sobreposição."""
    colheita = _buscar_dados_colheita(colheita_id)
    if not colheita:
        return {"erro": "Colheita não encontrada."}

    pontos = _buscar_pontos(colheita_id)
    if len(pontos) < 2:
        return {"erro": "Pontos insuficientes para análise."}

    distancia_total = 0.0
    sobreposicoes = []
    pontos_outros = _buscar_outras_maquinas(colheita_id)

    # cálculo de distância e sobreposição
    for i in range(1, len(pontos)):
        lat1, lon1 = pontos[i - 1]["lat"], pontos[i - 1]["lon"]
        lat2, lon2 = pontos[i]["lat"], pontos[i]["lon"]
        distancia_total += _calcular_distancia(lat1, lon1, lat2, lon2)

        for p in pontos_outros:
            if abs(lat2 - p["lat"]) < 0.00003 and abs(lon2 - p["lon"]) < 0.00003:
                sobreposicoes.append({
                    "lat": lat2,
                    "lon": lon2,
                    "outra_maquina": p["maquina_id"]
                })

    area_colhida = round((distancia_total * 5) / 10000, 2)
    maquinas_sobrepostas = list(set(p["outra_maquina"] for p in sobreposicoes))

    mapa_path = _gerar_mapa_trafego(colheita_id, colheita, pontos, sobreposicoes)

    return {
        "colheita": colheita,
        "distancia_total_km": round(distancia_total / 1000, 3),
        "area_colhida_ha": area_colhida,
        "qtd_sobreposicoes": len(sobreposicoes),
        "maquinas_sobrepostas": maquinas_sobrepostas,
        "status": "Atenção - Sobreposição detectada" if sobreposicoes else "Normal",
        "mapa": f"/{mapa_path.replace('app/', '')}"
    }
