from app.crud.colheitas import _buscar_pontos, _buscar_dados_colheita, _buscar_outras_maquinas, _calcular_distancia
from shapely.geometry import Point, Polygon
import folium

def gerar_mapa_trafego(colheita_id: int):
    """Gera um mapa interativo com áreas colhidas e sobreposições"""
    colheita = _buscar_dados_colheita(colheita_id)
    pontos = _buscar_pontos(colheita_id)
    outros = _buscar_outras_maquinas(colheita_id, colheita["maquina_id"])

    if not pontos:
        return {"erro": "Sem coordenadas para gerar mapa"}

    # base do mapa na posição média dos pontos
    lat_media = sum(p["lat"] for p in pontos) / len(pontos)
    lon_media = sum(p["lon"] for p in pontos) / len(pontos)
    mapa = folium.Map(location=[lat_media, lon_media], zoom_start=16)

    # desenha área da colheita principal
    folium.Polygon(
        locations=[(p["lat"], p["lon"]) for p in pontos],
        color="green", fill=True, fill_opacity=0.4,
        tooltip=f"Colheita {colheita_id} - Máquina {colheita['maquina']['modelo']}"
    ).add_to(mapa)

    # desenha áreas de outras máquinas
    for m in set(o["maquina_id"] for o in outros):
        pts = [(p["lat"], p["lon"]) for p in outros if p["maquina_id"] == m]
        if len(pts) > 2:
            folium.Polygon(
                locations=pts, color="blue", fill=True, fill_opacity=0.3,
                tooltip=f"Máquina {m}"
            ).add_to(mapa)

    # detecta sobreposição
    pol_principal = Polygon([(p["lat"], p["lon"]) for p in pontos])
    for m in set(o["maquina_id"] for o in outros):
        pts = [(p["lat"], p["lon"]) for p in outros if p["maquina_id"] == m]
        if len(pts) > 2:
            intersecao = pol_principal.intersection(Polygon(pts))
            if not intersecao.is_empty:
                folium.GeoJson(
                    intersecao.__geo_interface__,
                    style_function=lambda x: {"color": "red", "fillOpacity": 0.6},
                    tooltip=f"Sobreposição com Máquina {m}"
                ).add_to(mapa)

    mapa.save(f"mapa_colheita_{colheita_id}.html")
    return {"mapa": f"mapa_colheita_{colheita_id}.html", "colheita": colheita}