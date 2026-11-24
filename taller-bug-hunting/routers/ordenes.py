from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.database import obtener_bd
from models.mecanico import Mecanico as MecanicoModel
from models.orden import Orden as OrdenModel
from schemas.schemas import OrdenCreate, OrdenPatch, OrdenResponse

router = APIRouter(prefix="/ordenes", tags=["Órdenes"])


@router.post("/", status_code=201, response_model=OrdenResponse)
async def crear_orden(orden: OrdenCreate, db: AsyncSession = Depends(obtener_bd)):
    resultado_mec = await db.execute(
        select(MecanicoModel).where(MecanicoModel.id == orden.mecanico_id)
    )
    mecanico = resultado_mec.scalar_one_or_none()
    if not mecanico or not mecanico.activo:
        raise HTTPException(
            status_code=400,
            detail="El mecánico no existe o está desactivado",
        )

    nueva_orden = OrdenModel(**orden.model_dump())
    db.add(nueva_orden)
    await db.commit()

    resultado_orden = await db.execute(
        select(OrdenModel)
        .options(selectinload(OrdenModel.mecanico))
        .where(OrdenModel.id == nueva_orden.id)
    )
    return resultado_orden.scalar_one()


@router.get("/", response_model=List[OrdenResponse])
async def listar_ordenes(db: AsyncSession = Depends(obtener_bd)):
    resultado = await db.execute(
        select(OrdenModel).options(selectinload(OrdenModel.mecanico))
    )
    return resultado.scalars().all()


@router.patch("/{orden_id}", response_model=OrdenResponse)
async def actualizar_orden(
    orden_id: int,
    datos: OrdenPatch,
    db: AsyncSession = Depends(obtener_bd),
):
    resultado = await db.execute(
        select(OrdenModel)
        .options(selectinload(OrdenModel.mecanico))
        .where(OrdenModel.id == orden_id)
    )
    orden = resultado.scalar_one_or_none()
    if not orden:
        raise HTTPException(status_code=404, detail="Orden no encontrada")

    cambios = datos.model_dump(exclude_unset=True)
    for campo, valor in cambios.items():
        setattr(orden, campo, valor)

    await db.commit()
    await db.refresh(orden)
    return orden


@router.delete("/{orden_id}", status_code=204)
async def eliminar_orden(orden_id: int, db: AsyncSession = Depends(obtener_bd)):
    resultado = await db.execute(select(OrdenModel).where(OrdenModel.id == orden_id))
    orden = resultado.scalar_one_or_none()
    if not orden:
        raise HTTPException(status_code=404, detail="Orden no encontrada")

    await db.delete(orden)
    await db.commit()
    return None