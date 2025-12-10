from sqlalchemy.orm import Session
from . import models, schemas

def create_lead(db: Session, lead: schemas.LeadCreate):
    db_lead = models.Lead(**lead.dict())
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    return db_lead

def get_all_leads(db: Session):
    return db.query(models.Lead).all()

def get_lead(db: Session, lead_id: int):
    return db.query(models.Leaf).filter(models.Lead.id == lead_id).first()
