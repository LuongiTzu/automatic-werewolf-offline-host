"""Game schemas."""
from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel


class StartedPlayerResponse(BaseModel):
    id: str
    name: str
    is_alive: bool
    is_connected: bool
    is_ready: bool = False

    class Config:
        from_attributes = True


class StartGameResponse(BaseModel):
    room_code: str
    room_id: str
    status: str
    current_phase: str
    night_number: int
    day_number: int
    total_players: int
    message: str
    players: list[StartedPlayerResponse]

    class Config:
        from_attributes = True


class PlayerRoleResponse(BaseModel):
    player_id: str
    player_name: str
    room_id: str
    role_code: str
    role_name: str
    side: str
    description: Optional[str] = None
    night_order: Optional[int] = None

    class Config:
        from_attributes = True


class GameStateResponse(BaseModel):
    room_id: str
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


class NightActionRequest(BaseModel):
    player_id: str
    session_token: str
    action_type: str
    target_player_id: Optional[str] = None
    target_player_ids: Optional[list[str]] = None


class VoteRequest(BaseModel):
    voter_player_id: str
    session_token: str
    target_player_id: str


class AutoGameControlRequest(BaseModel):
    host_token: str


class GameLogResponse(BaseModel):
    id: str
    night_number: Optional[int] = None
    day_number: Optional[int] = None
    event_type: str
    message: str
    data: dict[str, Any]
    created_at: Optional[str] = None
