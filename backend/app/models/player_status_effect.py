"""Player status effects."""
from sqlalchemy import Boolean, Column, ForeignKey, String, UniqueConstraint

from app.models.base import BaseModel


class PlayerStatusEffect(BaseModel):
    """Stores extra role effects that are not part of the base player row."""
    __tablename__ = "player_status_effects"

    id = Column(String(36), primary_key=True, index=True)
    room_id = Column(String(36), ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False, index=True)
    player_id = Column(String(36), ForeignKey("players.id", ondelete="CASCADE"), nullable=False, index=True)

    is_oiled = Column(Boolean, default=False, nullable=False)
    is_cursed_wolf_activated = Column(Boolean, default=False, nullable=False)
    protected_last_night_by = Column(String(36), nullable=True)
    hunter_target_id = Column(String(36), nullable=True)

    __table_args__ = (
        UniqueConstraint("room_id", "player_id", name="uq_status_effect_player_per_room"),
    )
