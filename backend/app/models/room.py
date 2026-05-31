"""Room model."""
import enum

from sqlalchemy import Boolean, Column, DateTime, Enum as SQLEnum, Integer, String, Text

from app.models.base import BaseModel


class RoomStatus(str, enum.Enum):
    """Room status enum."""
    WAITING = "waiting"
    PLAYING = "playing"
    ENDED = "ended"


class GamePhase(str, enum.Enum):
    """Game phase enum for the automatic host flow."""
    SETUP = "setup"
    ROLE_REVEAL = "role_reveal"
    NIGHT_START = "night_start"
    NIGHT_ROLE_TURN = "night_role_turn"
    NIGHT_RESOLVING = "night_resolving"
    DAY_RESULT = "day_result"
    DAY_DISCUSSION = "day_discussion"
    VOTING = "voting"
    VOTE_RESULT = "vote_result"
    PAUSED = "paused"
    ENDED = "ended"

    # Backward-compatible aliases used by older frontend code.
    NIGHT = "night"
    DAY = "day"
    VOTE = "vote"


class Room(BaseModel):
    """Room model."""
    __tablename__ = "rooms"

    id = Column(String(36), primary_key=True, index=True)
    room_code = Column(String(6), unique=True, nullable=False, index=True)
    host_token = Column(String(64), unique=True, nullable=False)

    status = Column(SQLEnum(RoomStatus), default=RoomStatus.WAITING, nullable=False)
    current_phase = Column(SQLEnum(GamePhase), default=GamePhase.SETUP, nullable=False)

    # Existing counters kept for compatibility with current frontend.
    night_number = Column(Integer, default=0, nullable=False)
    day_number = Column(Integer, default=0, nullable=False)

    # Auto-host state.
    current_role_turn = Column(String(50), nullable=True)
    phase_ends_at = Column(DateTime, nullable=True)
    current_audio_text = Column(Text, nullable=True)
    is_paused = Column(Boolean, default=False, nullable=False)
    is_game_over = Column(Boolean, default=False, nullable=False)
    winner = Column(String(100), nullable=True)

    def __repr__(self):
        return f"<Room {self.room_code}>"
