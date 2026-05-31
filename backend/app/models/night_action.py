"""Night action model."""
from sqlalchemy import Column, ForeignKey, Integer, String, Text, UniqueConstraint

from app.models.base import BaseModel


class NightAction(BaseModel):
    """Stores one player's action during a night role turn."""
    __tablename__ = "night_actions"

    id = Column(String(36), primary_key=True, index=True)
    room_id = Column(String(36), ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False, index=True)
    night_number = Column(Integer, nullable=False, index=True)
    actor_player_id = Column(String(36), ForeignKey("players.id", ondelete="CASCADE"), nullable=False, index=True)
    actor_role_code = Column(String(50), nullable=False, index=True)
    action_type = Column(String(50), nullable=False, index=True)
    target_player_id = Column(String(36), ForeignKey("players.id", ondelete="SET NULL"), nullable=True)
    target_player_ids = Column(Text, nullable=True)  # JSON encoded list for advanced roles.

    __table_args__ = (
        UniqueConstraint(
            "room_id",
            "night_number",
            "actor_player_id",
            "action_type",
            name="uq_night_action_actor_type_per_night",
        ),
    )

    def __repr__(self):
        return f"<NightAction {self.action_type} by {self.actor_player_id}>"
