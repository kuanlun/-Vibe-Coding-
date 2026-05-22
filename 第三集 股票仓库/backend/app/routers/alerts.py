from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.alert import Alert
from app.models.user import User
from app.routers.auth import get_current_user

router = APIRouter()


class AlertCreate(BaseModel):
    symbol: str
    condition: str  # 高于/低于
    target_price: float


class AlertResponse(BaseModel):
    id: int
    user_id: int
    symbol: str
    condition: str
    target_price: float
    triggered: bool


@router.get("", response_model=list[AlertResponse])
def get_alerts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[Alert]:
    return db.query(Alert).filter(Alert.user_id == current_user.id).all()


@router.post("", response_model=AlertResponse)
def create_alert(
    alert: AlertCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Alert:
    if alert.condition not in ["高于", "低于"]:
        raise HTTPException(status_code=400, detail="Invalid condition")
    db_alert = Alert(
        user_id=current_user.id,
        symbol=alert.symbol,
        condition=alert.condition,
        target_price=alert.target_price,
    )
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert


@router.delete("/{alert_id}")
def delete_alert(
    alert_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict[str, str]:
    db_alert = (
        db.query(Alert)
        .filter(Alert.id == alert_id, Alert.user_id == current_user.id)
        .first()
    )
    if not db_alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    db.delete(db_alert)
    db.commit()
    return {"message": "Alert deleted"}