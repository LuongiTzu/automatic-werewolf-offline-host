"""Room API routers."""
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.services import PlayerService, RoleCartService, RoomService
from app.schemas import (
    CreateRoomResponse,
    JoinRoomRequest,
    JoinRoomResponse,
    PlayerInRoomResponse,
    RoleCartItemResponse,
    RoleCartResponse,
    RoomInfoResponse,
    UpdateRoleCartRequest,
)
from app.websocket.connection_manager import manager

router = APIRouter(prefix="/api/rooms", tags=["rooms"])


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def enum_to_value(value):
    return value.value if hasattr(value, "value") else value


def public_player(player) -> PlayerInRoomResponse:
    return PlayerInRoomResponse(
        id=player.id,
        name=player.name,
        is_alive=player.is_alive,
        is_connected=player.is_connected,
        is_ready=getattr(player, "is_ready", False),
    )


@router.post("/", response_model=CreateRoomResponse)
async def create_room(db: Session = Depends(get_db)):
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
    room = RoomService.get_room_by_code(db, room_code)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Room with code '{room_code}' not found")

    players = RoomService.get_room_players(db, room.id)
    return RoomInfoResponse(
        id=room.id,
        room_code=room.room_code,
        status=enum_to_value(room.status),
        current_phase=enum_to_value(room.current_phase),
        night_number=room.night_number,
        day_number=room.day_number,
        current_role_turn=room.current_role_turn,
        phase_ends_at=room.phase_ends_at,
        current_audio_text=room.current_audio_text,
        is_paused=room.is_paused,
        is_game_over=room.is_game_over,
        winner=room.winner,
        players=[public_player(p) for p in players],
        player_count=len(players),
        created_at=room.created_at,
    )


@router.post("/{room_code}/join", response_model=JoinRoomResponse)
async def join_room(room_code: str, request: JoinRoomRequest, db: Session = Depends(get_db)):
    if not request.name or not request.name.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Player name cannot be empty")
    if len(request.name.strip()) > 50:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Player name must be 50 characters or less")

    room = RoomService.get_room_by_code(db, room_code)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Room with code '{room_code}' not found")
    if enum_to_value(room.status) != "waiting":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Room is not accepting new players at this time")

    player = PlayerService.join_room(db, room.id, request.name.strip())
    player_count = RoomService.get_player_count(db, room.id)

    await manager.broadcast_room(
        room.room_code,
        {
            "type": "PLAYER_JOINED",
            "room_code": room.room_code,
            "payload": {
                "player": public_player(player).model_dump(mode="json"),
                "player_count": player_count,
            },
            "timestamp": now_iso(),
        },
    )

    return JoinRoomResponse(
        player_id=player.id,
        session_token=player.session_token,
        room_code=room.room_code,
        room_id=room.id,
        player_name=player.name,
        player_count=player_count,
        status=enum_to_value(room.status),
    )


@router.delete("/{room_id}/players/{player_id}")
async def kick_player(
    room_id: str,
    player_id: str,
    host_token: str = Header(..., alias="X-Host-Token"),
    db: Session = Depends(get_db),
):
    try:
        player = PlayerService.kick_player(db, room_id, player_id, host_token)
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    room = RoomService.get_room_by_id(db, room_id)
    if room:
        await manager.broadcast_room(
            room.room_code,
            {
                "type": "PLAYER_KICKED",
                "room_code": room.room_code,
                "payload": {"player_id": player_id, "player_name": player.name},
                "timestamp": now_iso(),
            },
        )
    return {"message": "Player kicked", "player_id": player_id}


@router.get("/{room_code}/role-cart", response_model=RoleCartResponse)
async def get_role_cart(room_code: str, db: Session = Depends(get_db)):
    room = RoomService.get_room_by_code(db, room_code)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Room with code '{room_code}' not found")

    summary = RoleCartService.get_cart_summary(db, room.id)
    return RoleCartResponse(
        room_code=room.room_code,
        room_id=room.id,
        cart=[RoleCartItemResponse(role_code=item["role_code"], name=item["name"], quantity=item["quantity"]) for item in summary["cart_items"]],
        total_roles=summary["total_roles"],
        total_players=summary["total_players"],
        can_start=summary["can_start"],
    )


@router.put("/{room_code}/role-cart", response_model=RoleCartResponse)
async def update_role_cart(room_code: str, request: UpdateRoleCartRequest, db: Session = Depends(get_db)):
    room = RoomService.get_room_by_code(db, room_code)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Room with code '{room_code}' not found")
    if enum_to_value(room.status) != "waiting":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can only update role cart when room is in 'waiting' status")

    try:
        roles_to_update = [{"role_code": r.role_code, "quantity": r.quantity} for r in request.roles]
        RoleCartService.update_cart(db, room.id, roles_to_update)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    summary = RoleCartService.get_cart_summary(db, room.id)
    response = RoleCartResponse(
        room_code=room.room_code,
        room_id=room.id,
        cart=[RoleCartItemResponse(role_code=item["role_code"], name=item["name"], quantity=item["quantity"]) for item in summary["cart_items"]],
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
