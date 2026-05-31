"""Role API routers"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import RoleService, RoleCartService, RoomService
from app.schemas import (
    RoleResponse,
    RoleCartResponse,
    RoleCartItemResponse,
    UpdateRoleCartRequest,
)

router = APIRouter(prefix="/api/roles", tags=["roles"])


@router.get("/", response_model=list[RoleResponse])
async def get_roles(db: Session = Depends(get_db)):
    """
    Get all available roles.
    
    Returns a list of all roles that can be used in the game.
    """
    roles = RoleService.get_all_roles(db, active_only=True)
    
    return [
        RoleResponse(
            code=role.code,
            name=role.name,
            side=role.side,
            description=role.description,
            night_order=role.night_order,
            is_active=role.is_active,
        )
        for role in roles
    ]
