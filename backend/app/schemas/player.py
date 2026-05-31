"""Player schemas"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PlayerResponse(BaseModel):
    """Player response schema"""
    id: str
    name: str
    room_id: str
    role_code: Optional[str] = None
    is_alive: bool
    is_connected: bool
    joined_at: datetime
    
    class Config:
        from_attributes = True


class PlayerInRoomResponse(BaseModel):
    """Player in room response (limited info)"""
    id: str
    name: str
    is_alive: bool
    is_connected: bool
    
    class Config:
        from_attributes = True
