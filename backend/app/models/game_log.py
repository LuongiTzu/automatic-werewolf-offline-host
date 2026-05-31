"""Game log model."""
from sqlalchemy import Column, ForeignKey, Integer, String, Text

from app.models.base import BaseModel


class GameLog(BaseModel):
    """Stores private game history for end-game review."""
    __tablename__ = "game_logs"

    id = Column(String(36), primary_key=True, index=True)
    room_id = Column(String(36), ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False, index=True)
    night_number = Column(Integer, nullable=True)
    day_number = Column(Integer, nullable=True)
    event_type = Column(String(50), nullable=False, index=True)
    message = Column(Text, nullable=False)
    data_json = Column(Text, nullable=True)
