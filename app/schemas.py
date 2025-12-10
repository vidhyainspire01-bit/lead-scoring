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
    score: Optional[float]
    band: Optional[str]
    model_version: Optional[str]
    created_at: datetime
    updated_at: datetime
    scored_at: Optional[datetime]

    class Config:
        from_attributes = True
