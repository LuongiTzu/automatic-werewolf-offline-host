"""Room schemas."""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

from app.schemas.player import PlayerInRoomResponse


class CreateRoomResponse(BaseModel):
    room_id: str
    room_code: str
    host_token: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class RoomInfoResponse(BaseModel):
    id: str
    room_code: str
    status: str
    current_phase: str
    night_number: int
    day_number: int
    current_role_turn: Optional[str] = None
    phase_ends_at: Optional[datetime] = None
    current_audio_text: Optional[str] = None
    is_paused: bool = False
    is_game_over: bool = False
    winner: Optional[str] = None
    players: List[PlayerInRoomResponse]
    player_count: int
    created_at: datetime

    class Config:
        from_attributes = True


class JoinRoomRequest(BaseModel):
    name: str

    class Config:
        json_schema_extra = {"example": {"name": "Nguyễn Văn A"}}


class JoinRoomResponse(BaseModel):
    player_id: str
    session_token: str
    room_code: str
    room_id: str
    player_name: str
    player_count: int
    status: str

    class Config:
        from_attributes = True
