"""Vote model."""
from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint

from app.models.base import BaseModel


class Vote(BaseModel):
    """Stores one player's day vote. One active vote per voter per day."""
    __tablename__ = "votes"

    id = Column(String(36), primary_key=True, index=True)
    room_id = Column(String(36), ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False, index=True)
    day_number = Column(Integer, nullable=False, index=True)
    voter_player_id = Column(String(36), ForeignKey("players.id", ondelete="CASCADE"), nullable=False, index=True)
    target_player_id = Column(String(36), ForeignKey("players.id", ondelete="CASCADE"), nullable=False, index=True)

    __table_args__ = (
        UniqueConstraint("room_id", "day_number", "voter_player_id", name="uq_vote_voter_per_day"),
    )

    def __repr__(self):
        return f"<Vote {self.voter_player_id} -> {self.target_player_id}>"
