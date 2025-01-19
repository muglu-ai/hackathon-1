from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    language = Column(String, default="en")

class Preference(Base):
    __tablename__ = "preferences"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    team = Column(String)
    player = Column(String)
    user = relationship("User", back_populates="preferences")

User.preferences = relationship("Preference", back_populates="user")


class Digest(Base):
    __tablename__ = "digests"

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, nullable=False)  # Game ID from the API
    summary = Column(Text, nullable=False)     # Digest summary
    language = Column(String(10), nullable=False, default="en")  # Language code
    video_url = Column(String, nullable=True)  # URL for video digest
    audio_url = Column(String, nullable=True)  # URL for audio digest
    created_at = Column(DateTime, default=datetime.utcnow)
