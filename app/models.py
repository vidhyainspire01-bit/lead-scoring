from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from .db import Base

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    country = Column(String)
    industry = Column(String)
    campaign = Column(String)
    budget = Column(Float)
    service = Column(String)
    activity_score = Column(Float)

    score = Column(Float, nullable=True)
    band = Column(String, nullable=True)
    model_version = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    scored_at = Column(DateTime, nullable=True)
