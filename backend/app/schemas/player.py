"""Player schemas."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class PlayerResponse(BaseModel):
    """Private player response schema."""
    id: str
    name: str
    room_id: str
    role_code: Optional[str] = None
    side: Optional[str] = None
    is_alive: bool
    is_connected: bool
    is_ready: bool = False
    is_host: bool = False
    created_at: datetime

    # Backward compatibility with older code that used joined_at in response.
    @property
    def joined_at(self) -> datetime:
        return self.created_at

    class Config:
        from_attributes = True


class PlayerInRoomResponse(BaseModel):
    """Public player info. Do not include role_code here."""
    id: str
    name: str
    is_alive: bool
    is_connected: bool
    is_ready: bool = False

    class Config:
        from_attributes = True
