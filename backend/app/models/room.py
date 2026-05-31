"""Room model"""
import enum

from sqlalchemy import Column, String, Integer, Enum as SQLEnum

from app.models.base import BaseModel


class RoomStatus(str, enum.Enum):
    """Room status enum"""
    WAITING = "waiting"
    PLAYING = "playing"
    ENDED = "ended"


class GamePhase(str, enum.Enum):
    """Game phase enum"""
    SETUP = "setup"
    NIGHT = "night"
    DAY = "day"
    VOTE = "vote"
    ENDED = "ended"


class Room(BaseModel):
    """Room model"""
    __tablename__ = "rooms"

    id = Column(String(36), primary_key=True, index=True)
    room_code = Column(String(6), unique=True, nullable=False, index=True)
    host_token = Column(String(64), unique=True, nullable=False)

    status = Column(
        SQLEnum(RoomStatus),
        default=RoomStatus.WAITING,
        nullable=False,
    )

    current_phase = Column(
        SQLEnum(GamePhase),
        default=GamePhase.SETUP,
        nullable=False,
    )

    night_number = Column(Integer, default=0, nullable=False)
    day_number = Column(Integer, default=0, nullable=False)

    def __repr__(self):
        return f"<Room {self.room_code}>"