from fastapi import APIRouter, Depends, HTTPException
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

    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    # Run scoring
    score = score_lead(lead)
    band = band_from_score(score)

    # Update in DB
    lead.score = score
    lead.band = band
    lead.model_version = "uc_prod"
    db.commit()
    db.refresh(lead)

    return {
        "lead_id": lead_id,
        "score": score,
        "band": band,
        "model_version": "local_v1"
    }


# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from ..db import SessionLocal
# from ..ml.score import score_lead, band_from_score
# from ..models import Lead

# router = APIRouter()


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# @router.post("/score/{lead_id}")
# def score_lead_api(lead_id: int, db: Session = Depends(get_db)):
#     lead = db.query(Lead).filter(Lead.id == lead_id).first()

#     if not lead:
#         raise HTTPException(status_code=404, detail="Lead not found")

#     # Score using UC model
#     score = score_lead(lead)
#     band = band_from_score(score)

#     lead.score = score
#     lead.band = band
#     lead.model_version = "uc_prod"
#     db.commit()
#     db.refresh(lead)

#     return {
#         "lead_id": lead_id,
#         "score": score,
#         "band": band,
#         "model_version": "uc_prod"
#     }
