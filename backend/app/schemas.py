from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LeadCreate(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    country: Optional[str] = None
    industry: Optional[str] = None
    campaign: Optional[str] = None
    budget: Optional[float] = None
    service: Optional[str] = None
    activity_score: Optional[float] = None

class LeadResponse(LeadCreate):
    id: int
    score: Optional[float] = None
    band: Optional[str] = None
    model_version: Optional[str] = None
    created_at: Optional[datetime]
    scored_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True   # replaces orm_mode = True
