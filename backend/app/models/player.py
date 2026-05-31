"""Player model."""
from sqlalchemy import Boolean, Column, ForeignKey, String

from app.models.base import BaseModel


class Player(BaseModel):
    """Player model."""
    __tablename__ = "players"

    id = Column(String(36), primary_key=True, index=True)
    room_id = Column(String(36), ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(50), nullable=False)
    session_token = Column(String(64), unique=True, nullable=False, index=True)

    # Secret role data. Never broadcast role_code to all players while game is running.
    role_code = Column(String(50), nullable=True)
    side = Column(String(50), nullable=True)

    is_alive = Column(Boolean, default=True, nullable=False)
    is_connected = Column(Boolean, default=True, nullable=False)
    is_ready = Column(Boolean, default=False, nullable=False)
    is_host = Column(Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"<Player {self.name} in Room {self.room_id}>"
