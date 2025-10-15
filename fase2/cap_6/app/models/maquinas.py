from pydantic import BaseModel, Field, validator
from typing import Optional
import re
from datetime import date

CURRENT_YEAR = date.today().year
ACCEPTED_CHARS_REGEX = r'^[\w\sÀ-ÿ]+$'

class MaquinaCreate(BaseModel):
    modelo: str = Field(..., min_length=3, max_length=100)
    tipo: str = Field(..., min_length=3, max_length=50)
    ano_fabricacao: Optional[int] = Field(None, ge=1900, le=CURRENT_YEAR)
    status: Optional[bool] = True

    @validator('modelo', 'tipo')
    def only_letters_numbers_spaces(cls, v):
        if not re.match(ACCEPTED_CHARS_REGEX, v):
            raise ValueError('Somente letras (acentuadas), números e espaços são permitidos')
        return v

class MaquinaUpdate(BaseModel):
    modelo: Optional[str] = Field(None, min_length=3, max_length=100)
    tipo: Optional[str] = Field(None, min_length=3, max_length=50)
    ano_fabricacao: Optional[int] = Field(None, ge=1900, le=CURRENT_YEAR)
    status: Optional[bool] = None

    @validator('modelo', 'tipo')
    def only_letters_numbers_spaces(cls, v):
        if v is not None and not re.match(ACCEPTED_CHARS_REGEX, v):
            raise ValueError('Somente letras (acentuadas), números e espaços são permitidos')
        return v

class MaquinaOut(BaseModel):
    id: int
    modelo: str
    tipo: str
    ano_fabricacao: Optional[int] = None
    status: bool
