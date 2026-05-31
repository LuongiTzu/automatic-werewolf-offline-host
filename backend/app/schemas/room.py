"""Room schemas"""
from datetime import datetime
from typing import List

from pydantic import BaseModel

from app.schemas.player import PlayerInRoomResponse


class CreateRoomResponse(BaseModel):
    """Create room response schema"""
    room_id: str
    room_code: str
    host_token: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class RoomInfoResponse(BaseModel):
    """Room info response schema"""
    id: str
    room_code: str
    status: str
    current_phase: str
    night_number: int
    day_number: int
    players: List[PlayerInRoomResponse]
    player_count: int
    created_at: datetime

    class Config:
        from_attributes = True


class JoinRoomRequest(BaseModel):
    """Join room request schema"""
    name: str

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Nguyễn Văn A"
            }
        }


class JoinRoomResponse(BaseModel):
    """Join room response schema"""
    player_id: str
    session_token: str
    room_code: str
    room_id: str
    player_name: str
    player_count: int
    status: str

    class Config:
        from_attributes = True