"""Player model"""
from sqlalchemy import Column, String, Boolean, ForeignKey, Integer
from app.models.base import BaseModel


class Player(BaseModel):
    """Player model"""
    __tablename__ = "players"
    
    id = Column(String(36), primary_key=True, index=True)
    room_id = Column(String(36), ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(50), nullable=False)
    session_token = Column(String(64), unique=True, nullable=False, index=True)
    role_code = Column(String(50), nullable=True)  # e.g., "werewolf", "villager", "protector"
    is_alive = Column(Boolean, default=True, nullable=False)
    is_connected = Column(Boolean, default=True, nullable=False)
    
    def __repr__(self):
        return f"<Player {self.name} in Room {self.room_id}>"
