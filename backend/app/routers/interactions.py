from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.interaction import Interaction
from app.schemas.interaction import InteractionCreate, InteractionUpdate, InteractionRead

router = APIRouter(prefix="/api/interactions", tags=["interactions"])


@router.post("", response_model=InteractionRead, status_code=201)
def create_interaction(data: InteractionCreate, db: Session = Depends(get_db)):
    interaction = Interaction(**data.model_dump())
    db.add(interaction)
    db.commit()
    db.refresh(interaction)
    return interaction


@router.get("", response_model=list[InteractionRead])
def list_interactions(hcp_id: str | None = None, db: Session = Depends(get_db)):
    query = db.query(Interaction)
    if hcp_id:
        query = query.filter(Interaction.hcp_id == hcp_id)
    return query.order_by(Interaction.created_at.desc()).limit(50).all()


@router.get("/{interaction_id}", response_model=InteractionRead)
def get_interaction(interaction_id: str, db: Session = Depends(get_db)):
    interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    return interaction


@router.patch("/{interaction_id}", response_model=InteractionRead)
def update_interaction(interaction_id: str, data: InteractionUpdate, db: Session = Depends(get_db)):
    interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(interaction, field, value)
    db.commit()
    db.refresh(interaction)
    return interaction


@router.delete("/{interaction_id}", status_code=204)
def delete_interaction(interaction_id: str, db: Session = Depends(get_db)):
    interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    db.delete(interaction)
    db.commit()
