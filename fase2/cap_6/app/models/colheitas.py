from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ColheitaBase(BaseModel):
    maquina_id: int
    inicio: Optional[datetime] = None
    fim: Optional[datetime] = None
    area_colhida: Optional[float] = None
    duracao: Optional[float] = None
    status: Optional[str] = None

class ColheitaCreate(BaseModel):
    maquina_id: int

class ColheitaResponse(ColheitaBase):
    id: int

    class Config:
        orm_mode = True
