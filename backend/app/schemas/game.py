"""Game schemas"""

from typing import Optional
from pydantic import BaseModel


class StartedPlayerResponse(BaseModel):
    """Player info returned after game start.

    Important:
    - Do not return role_code here.
    - Role is secret and must be fetched only by the correct player using session_token.
    """

    id: str
    name: str
    is_alive: bool
    is_connected: bool

    class Config:
        from_attributes = True


class StartGameResponse(BaseModel):
    """Start game response schema"""

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
    """Private role response for one player"""

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