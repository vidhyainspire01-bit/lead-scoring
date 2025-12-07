from sqlalchemy import Column, Integer, String, Numeric, TIMESTAMP
from sqlalchemy.sql import func
from .db import Base

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String)
    phone = Column(String)
    country = Column(String)
    industry = Column(String)
    campaign = Column(String)
    budget = Column(Numeric)
    service = Column(String)
    activity_score = Column(Numeric)
    score = Column(Numeric)
    band = Column(String)
    model_version = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())
    scored_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
