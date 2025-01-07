# app/models/digest.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from database import Base
from datetime import datetime

class Digest(Base):
    __tablename__ = "digests"

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, nullable=False)  # Game ID from the API
    summary = Column(Text, nullable=False)     # Digest summary
    language = Column(String(10), nullable=False, default="en")  # Language code
    created_at = Column(DateTime, default=datetime.utcnow)
