from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import obtener_bd
from models.mecanico import Mecanico as MecanicoModel
from schemas.schemas import MecanicoCreate, MecanicoResponse

router = APIRouter(prefix="/mecanicos", tags=["Mecánicos"])


@router.post("/", status_code=201, response_model=MecanicoResponse)
async def crear_mecanico(mecanico: MecanicoCreate, db: AsyncSession = Depends(obtener_bd)):
    nuevo = MecanicoModel(**mecanico.model_dump())
    db.add(nuevo)
    await db.commit()
    await db.refresh(nuevo)
    return nuevo


@router.get("/", response_model=List[MecanicoResponse])
async def listar_mecanicos(db: AsyncSession = Depends(obtener_bd)):
    resultado = await db.execute(
        select(MecanicoModel).where(MecanicoModel.activo.is_(True))
    )
    return resultado.scalars().all()


@router.delete("/{mecanico_id}", status_code=204)
async def desactivar_mecanico(mecanico_id: int, db: AsyncSession = Depends(obtener_bd)):
    resultado = await db.execute(
        select(MecanicoModel).where(MecanicoModel.id == mecanico_id)
    )
    mecanico = resultado.scalar_one_or_none()
    if not mecanico:
        raise HTTPException(status_code=404, detail="Mecánico no encontrado")

    mecanico.activo = False
    await db.commit()
    return None