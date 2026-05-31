"""Room API routers"""

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.services import RoomService, PlayerService, RoleCartService
from app.schemas import (
    CreateRoomResponse,
    RoomInfoResponse,
    JoinRoomRequest,
    JoinRoomResponse,
    PlayerInRoomResponse,
    RoleCartResponse,
    RoleCartItemResponse,
    UpdateRoleCartRequest,
)
from app.websocket.connection_manager import manager

router = APIRouter(prefix="/api/rooms", tags=["rooms"])


def now_iso() -> str:
    """Return current UTC time in ISO format."""
    return datetime.now(timezone.utc).isoformat()


def enum_to_value(value):
    """Convert enum value to plain string if needed."""
    return value.value if hasattr(value, "value") else value


@router.post("/", response_model=CreateRoomResponse)
async def create_room(db: Session = Depends(get_db)):
    """
    Create a new game room.

    - **Returns**: room_code (6 chars), host_token, and room_id
    - Host uses room_code to share with players
    - Host uses host_token to authenticate commands
    """
    room = RoomService.create_room(db)

    return CreateRoomResponse(
        room_id=room.id,
        room_code=room.room_code,
        host_token=room.host_token,
        status=enum_to_value(room.status),
        created_at=room.created_at,
    )


@router.get("/{room_code}", response_model=RoomInfoResponse)
async def get_room(room_code: str, db: Session = Depends(get_db)):
    """
    Get room information and player list.

    - **room_code**: The 6-character room code
    - Returns room status, current phase, and all players in the room
    """
    room = RoomService.get_room_by_code(db, room_code)

    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Room with code '{room_code}' not found",
        )

    players = RoomService.get_room_players(db, room.id)
    player_count = len(players)

    players_response = [
        PlayerInRoomResponse(
            id=p.id,
            name=p.name,
            is_alive=p.is_alive,
            is_connected=p.is_connected,
        )
        for p in players
    ]

    return RoomInfoResponse(
        id=room.id,
        room_code=room.room_code,
        status=enum_to_value(room.status),
        current_phase=enum_to_value(room.current_phase),
        night_number=room.night_number,
        day_number=room.day_number,
        players=players_response,
        player_count=player_count,
        created_at=room.created_at,
    )


@router.post("/{room_code}/join", response_model=JoinRoomResponse)
async def join_room(
    room_code: str,
    request: JoinRoomRequest,
    db: Session = Depends(get_db),
):
    """
    Player joins a room.

    - **room_code**: The 6-character room code to join
    - **name**: Player's display name
    - Returns player_id, session_token, and room info
    - Player uses session_token to authenticate their actions
    """
    if not request.name or len(request.name.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Player name cannot be empty",
        )

    if len(request.name) > 50:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Player name must be 50 characters or less",
        )

    room = RoomService.get_room_by_code(db, room_code)

    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Room with code '{room_code}' not found",
        )

    if enum_to_value(room.status) != "waiting":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Room is not accepting new players at this time",
        )

    player = PlayerService.join_room(db, room.id, request.name.strip())

    player_count = RoomService.get_player_count(db, room.id)

    response = JoinRoomResponse(
        player_id=player.id,
        session_token=player.session_token,
        room_code=room.room_code,
        room_id=room.id,
        player_name=player.name,
        player_count=player_count,
        status=enum_to_value(room.status),
    )

    await manager.broadcast_room(
        room.room_code,
        {
            "type": "PLAYER_JOINED",
            "room_code": room.room_code,
            "payload": {
                "player": {
                    "id": player.id,
                    "name": player.name,
                    "is_alive": player.is_alive,
                    "is_connected": player.is_connected,
                },
                "player_count": player_count,
            },
            "timestamp": now_iso(),
        },
    )

    return response


@router.get("/{room_code}/role-cart", response_model=RoleCartResponse)
async def get_role_cart(room_code: str, db: Session = Depends(get_db)):
    """
    Get the role cart for a room.

    - **room_code**: The 6-character room code
    - Returns the current role selections and whether game can start
    - **can_start**: true if total_roles >= total_players
    """
    room = RoomService.get_room_by_code(db, room_code)

    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Room with code '{room_code}' not found",
        )

    summary = RoleCartService.get_cart_summary(db, room.id)

    cart_items = [
        RoleCartItemResponse(
            role_code=item["role_code"],
            name=item["name"],
            quantity=item["quantity"],
        )
        for item in summary["cart_items"]
    ]

    return RoleCartResponse(
        room_code=room.room_code,
        room_id=room.id,
        cart=cart_items,
        total_roles=summary["total_roles"],
        total_players=summary["total_players"],
        can_start=summary["can_start"],
    )


@router.put("/{room_code}/role-cart", response_model=RoleCartResponse)
async def update_role_cart(
    room_code: str,
    request: UpdateRoleCartRequest,
    db: Session = Depends(get_db),
):
    """
    Update the role cart for a room.

    - **room_code**: The 6-character room code
    - **roles**: List of roles with quantities to set
    - Returns updated cart with validation status
    """
    room = RoomService.get_room_by_code(db, room_code)

    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Room with code '{room_code}' not found",
        )

    if enum_to_value(room.status) != "waiting":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only update role cart when room is in 'waiting' status",
        )

    try:
        roles_to_update = [
            {"role_code": r.role_code, "quantity": r.quantity}
            for r in request.roles
        ]
        RoleCartService.update_cart(db, room.id, roles_to_update)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    summary = RoleCartService.get_cart_summary(db, room.id)

    cart_items = [
        RoleCartItemResponse(
            role_code=item["role_code"],
            name=item["name"],
            quantity=item["quantity"],
        )
        for item in summary["cart_items"]
    ]

    response = RoleCartResponse(
        room_code=room.room_code,
        room_id=room.id,
        cart=cart_items,
        total_roles=summary["total_roles"],
        total_players=summary["total_players"],
        can_start=summary["can_start"],
    )

    await manager.broadcast_room(
        room.room_code,
        {
            "type": "ROLE_CART_UPDATED",
            "room_code": room.room_code,
            "payload": response.model_dump(mode="json"),
            "timestamp": now_iso(),
        },
    )

    return response