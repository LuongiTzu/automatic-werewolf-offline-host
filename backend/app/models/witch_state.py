"""Witch potion state."""
from sqlalchemy import Boolean, Column, ForeignKey, String, UniqueConstraint

from app.models.base import BaseModel


class WitchState(BaseModel):
    """Tracks witch potions for one witch player in one room."""
    __tablename__ = "witch_states"

    id = Column(String(36), primary_key=True, index=True)
    room_id = Column(String(36), ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False, index=True)
    player_id = Column(String(36), ForeignKey("players.id", ondelete="CASCADE"), nullable=False, index=True)
    healing_potion_available = Column(Boolean, default=True, nullable=False)
    poison_potion_available = Column(Boolean, default=True, nullable=False)

    __table_args__ = (
        UniqueConstraint("room_id", "player_id", name="uq_witch_state_player_per_room"),
    )
