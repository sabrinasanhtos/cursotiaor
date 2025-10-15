from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.routers.maquinas import router as maquinas_router
from app.routers.colheitas import router as colheitas_router
from app.routers.relatorios import router as relatorios_router

app = FastAPI(title="Controle de Tráfego de Máquinas na Colheita de Cana")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/maquinas", response_class=HTMLResponse)
def view_maquinas(request: Request):
    return templates.TemplateResponse("maquinas.html", {"request": request})

@app.get("/relatorios", response_class=HTMLResponse)
def view_relatorios(request: Request):
    return templates.TemplateResponse("relatorios.html", {"request": request})

@app.get("/colheitas", response_class=HTMLResponse)
def view_colheitas(request: Request):
    return templates.TemplateResponse("colheitas.html", {"request": request})

app.include_router(maquinas_router)
app.include_router(colheitas_router)
app.include_router(relatorios_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)