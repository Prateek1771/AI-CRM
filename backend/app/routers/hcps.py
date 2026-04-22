from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.hcp import HCP
from app.schemas.hcp import HCPCreate, HCPRead

router = APIRouter(prefix="/api/hcps", tags=["hcps"])


@router.get("", response_model=list[HCPRead])
def list_hcps(q: str | None = Query(None), db: Session = Depends(get_db)):
    query = db.query(HCP)
    if q:
        query = query.filter(HCP.name.ilike(f"%{q}%"))
    return query.limit(20).all()


@router.post("", response_model=HCPRead, status_code=201)
def create_hcp(data: HCPCreate, db: Session = Depends(get_db)):
    hcp = HCP(**data.model_dump())
    db.add(hcp)
    db.commit()
    db.refresh(hcp)
    return hcp


@router.get("/{hcp_id}", response_model=HCPRead)
def get_hcp(hcp_id: str, db: Session = Depends(get_db)):
    hcp = db.query(HCP).filter(HCP.id == hcp_id).first()
    if not hcp:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="HCP not found")
    return hcp
