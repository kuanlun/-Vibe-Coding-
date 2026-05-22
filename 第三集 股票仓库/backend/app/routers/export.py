from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import csv
import io

from app.database import get_db
from app.models.portfolio import Portfolio
from app.models.user import User
from app.routers.auth import get_current_user

router = APIRouter()


@router.get("/excel")
def export_excel(
    market: Annotated[str | None, Query()] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict[str, str]:
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.get("/csv")
def export_csv(
    market: Annotated[str | None, Query()] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> StreamingResponse:
    query = db.query(Portfolio).filter(Portfolio.user_id == current_user.id)
    if market:
        query = query.filter(Portfolio.market == market)
    portfolios = query.all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Market", "Symbol", "Name", "Shares", "Cost Price", "Created At"])
    for p in portfolios:
        writer.writerow([p.market, p.symbol, p.name, p.shares, p.cost_price, p.created_at])

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=portfolios.csv"},
    )