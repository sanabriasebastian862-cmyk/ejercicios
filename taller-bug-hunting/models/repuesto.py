from sqlalchemy import Column, Integer, String, Float
from core.database import Base

class Repuesto(Base):
    __tablename__ = "repuestos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    precio_venta = Column(Float, nullable=False)
    stock_actual = Column(Integer, default=0)