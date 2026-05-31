"""Game API routers"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.services import GameStartService
from app.services.room_service import RoomService
from app.schemas import (
    StartGameResponse,
    StartedPlayerResponse,
    PlayerRoleResponse,
)

router = APIRouter(prefix="/api", tags=["game"])


@router.post("/rooms/{room_code}/start", response_model=StartGameResponse)
async def start_game(room_code: str, db: Session = Depends(get_db)):
    """
    Start a room game and assign roles.

    Rules:
    - Room must exist.
    - Room must be in waiting status.
    - There must be at least 1 player.
    - Total roles must be >= total players.
    - Role cart must include at least 1 WEREWOLF.
    - Response does not expose player roles.
    """
    try:
        room = GameStartService.start_game(db, room_code)
    except ValueError as e:
        message = str(e)

        if "not found" in message.lower():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=message,
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
        )

    players = RoomService.get_room_players(db, room.id)

    players_response = [
        StartedPlayerResponse(
            id=player.id,
            name=player.name,
            is_alive=player.is_alive,
            is_connected=player.is_connected,
        )
        for player in players
    ]

    return StartGameResponse(
        room_code=room.room_code,
        room_id=room.id,
        status=room.status.value if hasattr(room.status, "value") else str(room.status),
        current_phase=room.current_phase.value
        if hasattr(room.current_phase, "value")
        else str(room.current_phase),
        night_number=room.night_number,
        day_number=room.day_number,
        total_players=len(players),
        message="Game started successfully. Roles have been assigned.",
        players=players_response,
    )


@router.get("/players/{player_id}/role", response_model=PlayerRoleResponse)
async def get_my_role(
    player_id: str,
    session_token: str = Query(..., description="Player session token"),
    db: Session = Depends(get_db),
):
    """
    Get the private role of one player.

    Security:
    - The player must provide their own session_token.
    - This endpoint must not expose other players' roles.
    """
    try:
        role_info = GameStartService.get_player_role(
            db=db,
            player_id=player_id,
            session_token=session_token,
        )
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )
    except ValueError as e:
        message = str(e)

        if "not found" in message.lower():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=message,
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
        )

    return PlayerRoleResponse(**role_info)