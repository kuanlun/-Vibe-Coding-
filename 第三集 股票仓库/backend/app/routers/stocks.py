from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.routers.auth import get_current_user

router = APIRouter()


class StockQuote(BaseModel):
    symbol: str
    name: str
    price: float
    change: float
    change_percent: float
    market: str


@router.get("/quote/{symbol}", response_model=StockQuote)
def get_quote(
    symbol: str,
    current_user: User = Depends(get_current_user),
) -> StockQuote:
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.post("/batch", response_model=list[StockQuote])
def get_batch_quotes(
    symbols: list[str],
    current_user: User = Depends(get_current_user),
) -> list[StockQuote]:
    raise HTTPException(status_code=501, detail="Not implemented yet")