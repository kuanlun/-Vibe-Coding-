from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.portfolio import Portfolio
from app.models.user import User
from app.routers.auth import get_current_user

router = APIRouter()


class PortfolioCreate(BaseModel):
    market: str
    symbol: str
    name: str
    shares: float
    cost_price: float


class PortfolioUpdate(BaseModel):
    market: str | None = None
    symbol: str | None = None
    name: str | None = None
    shares: float | None = None
    cost_price: float | None = None


class PortfolioResponse(BaseModel):
    id: int
    user_id: int
    market: str
    symbol: str
    name: str
    shares: float
    cost_price: float


@router.get("", response_model=list[PortfolioResponse])
def get_portfolios(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[Portfolio]:
    return (
        db.query(Portfolio)
        .filter(Portfolio.user_id == current_user.id)
        .order_by(Portfolio.market)
        .all()
    )


@router.post("", response_model=PortfolioResponse)
def create_portfolio(
    portfolio: PortfolioCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Portfolio:
    db_portfolio = Portfolio(
        user_id=current_user.id,
        market=portfolio.market,
        symbol=portfolio.symbol,
        name=portfolio.name,
        shares=portfolio.shares,
        cost_price=portfolio.cost_price,
    )
    db.add(db_portfolio)
    db.commit()
    db.refresh(db_portfolio)
    return db_portfolio


@router.put("/{portfolio_id}", response_model=PortfolioResponse)
def update_portfolio(
    portfolio_id: int,
    portfolio_update: PortfolioUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Portfolio:
    db_portfolio = (
        db.query(Portfolio)
        .filter(Portfolio.id == portfolio_id, Portfolio.user_id == current_user.id)
        .first()
    )
    if not db_portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    if portfolio_update.market is not None:
        db_portfolio.market = portfolio_update.market
    if portfolio_update.symbol is not None:
        db_portfolio.symbol = portfolio_update.symbol
    if portfolio_update.name is not None:
        db_portfolio.name = portfolio_update.name
    if portfolio_update.shares is not None:
        db_portfolio.shares = portfolio_update.shares
    if portfolio_update.cost_price is not None:
        db_portfolio.cost_price = portfolio_update.cost_price
    db.commit()
    db.refresh(db_portfolio)
    return db_portfolio


@router.delete("/{portfolio_id}")
def delete_portfolio(
    portfolio_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict[str, str]:
    db_portfolio = (
        db.query(Portfolio)
        .filter(Portfolio.id == portfolio_id, Portfolio.user_id == current_user.id)
        .first()
    )
    if not db_portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    db.delete(db_portfolio)
    db.commit()
    return {"message": "Portfolio deleted"}