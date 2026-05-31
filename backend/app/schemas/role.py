"""Role schemas"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class RoleResponse(BaseModel):
    """Role response schema"""
    code: str
    name: str
    side: str
    description: Optional[str] = None
    night_order: Optional[int] = None
    is_active: bool
    
    class Config:
        from_attributes = True


class RoleCartItemRequest(BaseModel):
    """Single role cart item request"""
    role_code: str
    quantity: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "role_code": "VILLAGER",
                "quantity": 5
            }
        }


class RoleCartItemResponse(BaseModel):
    """Single role cart item response"""
    role_code: str
    name: str
    quantity: int
    
    class Config:
        from_attributes = True


class RoleCartResponse(BaseModel):
    """Role cart response schema"""
    room_code: str
    room_id: str
    cart: list[RoleCartItemResponse]
    total_roles: int
    total_players: int
    can_start: bool  # true if total_roles >= total_players
    
    class Config:
        from_attributes = True


class UpdateRoleCartRequest(BaseModel):
    """Update role cart request"""
    roles: list[RoleCartItemRequest]
    
    class Config:
        json_schema_extra = {
            "example": {
                "roles": [
                    {"role_code": "VILLAGER", "quantity": 5},
                    {"role_code": "WEREWOLF", "quantity": 2},
                    {"role_code": "SEER", "quantity": 1},
                ]
            }
        }
