from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base
from app.routers import auth, portfolios, stocks, alerts, export
from app.database import engine

app = FastAPI(title="Stock Portfolio Manager", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(portfolios.router, prefix="/api/portfolios", tags=["portfolios"])
app.include_router(stocks.router, prefix="/api/stocks", tags=["stocks"])
app.include_router(alerts.router, prefix="/api/alerts", tags=["alerts"])
app.include_router(export.router, prefix="/api/export", tags=["export"])


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Stock Portfolio Manager API"}