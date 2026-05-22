from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from app.database import Base


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    symbol = Column(String(20), nullable=False)
    condition = Column(String(10), nullable=False)  # 高于/低于
    target_price = Column(Float, nullable=False)
    triggered = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)