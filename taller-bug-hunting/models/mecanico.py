from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from core.database import Base

class Mecanico(Base):
    __tablename__ = "mecanicos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre_completo = Column(String(100), nullable=False)
    especialidad = Column(String(50), nullable=False)
    activo = Column(Boolean, default=True)

    ordenes = relationship("Orden", back_populates="mecanico")