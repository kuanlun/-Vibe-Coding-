from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    market = Column(String(10), nullable=False)  # A股/台股/美股
    symbol = Column(String(20), nullable=False)
    name = Column(String(50), nullable=False)
    shares = Column(Float, nullable=False)
    cost_price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)