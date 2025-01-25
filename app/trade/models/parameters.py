# app/models/parameter.py
from sqlalchemy import Column, Integer, String, DateTime, Numeric
from app.db.base_class import Base

class Parameters(Base):
    id = Column(Integer, primary_key=True, index=True)
    a_value = Column(Numeric(8,4))
    b_value = Column(Numeric(8,4))
    c_value = Column(Integer)
    updated_at = Column(DateTime)
