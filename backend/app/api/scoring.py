from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import SessionLocal
from ..ml.score import score_lead, band_from_score
from ..models import Lead

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/score/{lead_id}")
def score_lead_api(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()

    s = score_lead(lead)
    b = band_from_score(s)

    lead.score = s
    lead.band = b
    lead.model_version = "v1"
    db.commit()
    db.refresh(lead)

    return {"score": s, "band": b, "model_version": "v1"}
@router.post("/score/batch")
def score_leads_api(lead_ids: list[int], db: Session = Depends(get_db)):
    results = []
    for lead_id in lead_ids:
        lead = db.query(Lead).filter(Lead.id == lead_id).first()
        s = score_lead(lead)
        b = band_from_score(s)

        lead.score = s
        lead.band = b
        lead.model_version = "v1"
        db.commit()
        db.refresh(lead)

        results.append({"lead_id": lead_id, "score": s, "band": b, "model_version": "v1"})
    return results