from typing import List, Optional
from pydantic import BaseModel, Field


class MecanicoCreate(BaseModel):
    nombre_completo: str
    especialidad: str


class MecanicoResumen(BaseModel):
    id: int
    nombre_completo: str
    especialidad: str
    activo: bool

    model_config = {"from_attributes": True}


class OrdenCreate(BaseModel):
    placa: str = Field(..., min_length=5, max_length=6)
    modelo: str
    falla_reportada: str
    mecanico_id: int


class OrdenPatch(BaseModel):
    estado: Optional[str] = None
    costo_reparacion: Optional[float] = Field(None, ge=0)
    falla_reportada: Optional[str] = None


class OrdenResponse(OrdenCreate):
    id: int
    estado: str
    costo_reparacion: float
    mecanico: Optional[MecanicoResumen] = None

    model_config = {"from_attributes": True}


class MecanicoResponse(MecanicoCreate):
    id: int
    activo: bool
    ordenes: List[OrdenResponse] = []

    model_config = {"from_attributes": True}