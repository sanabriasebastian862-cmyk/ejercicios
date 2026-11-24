from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from core.database import Base


class Orden(Base):
    __tablename__ = "ordenes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    placa = Column(String(10), nullable=False)
    modelo = Column(String(100), nullable=False)
    falla_reportada = Column(String(255), nullable=False)
    estado = Column(String(30), default="Abierta", nullable=False)
    costo_reparacion = Column(Float, default=0.0, nullable=False)
    mecanico_id = Column(Integer, ForeignKey("mecanicos.id"), nullable=False)

    mecanico = relationship("Mecanico", back_populates="ordenes")