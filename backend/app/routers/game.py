"""Game API routers."""
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Header, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.game_engine.auto_orchestrator import AutoGameOrchestrator
from app.models import GamePhase, Room, RoomStatus
from app.schemas import (
    AutoGameControlRequest,
    GameStateResponse,
    NightActionRequest,
    PlayerRoleResponse,
    StartedPlayerResponse,
    StartGameResponse,
    VoteRequest,
)
from app.services import GameLogService, GameStartService, NightActionService, RoomService, VoteService
from app.websocket.connection_manager import manager

router = APIRouter(prefix="/api", tags=["game"])


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def enum_to_value(value):
    return value.value if hasattr(value, "value") else value


def state_response(room: Room) -> GameStateResponse:
    return GameStateResponse(
        room_id=room.id,
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
    )


@router.post("/rooms/{room_code}/start", response_model=StartGameResponse)
async def start_game(room_code: str, db: Session = Depends(get_db)):
    try:
        room = GameStartService.start_game(db, room_code)
    except ValueError as e:
        message = str(e)
        if "not found" in message.lower():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

    players = RoomService.get_room_players(db, room.id)
    players_response = [
        StartedPlayerResponse(
            id=player.id,
            name=player.name,
            is_alive=player.is_alive,
            is_connected=player.is_connected,
            is_ready=getattr(player, "is_ready", False),
        )
        for player in players
    ]

    response = StartGameResponse(
        room_code=room.room_code,
        room_id=room.id,
        status=enum_to_value(room.status),
        current_phase=enum_to_value(room.current_phase),
        night_number=room.night_number,
        day_number=room.day_number,
        total_players=len(players),
        message="Game started successfully. Roles have been assigned.",
        players=players_response,
    )

    await manager.broadcast_room(
        room.room_code,
        {
            "type": "GAME_STARTED",
            "room_code": room.room_code,
            "payload": response.model_dump(mode="json"),
            "timestamp": now_iso(),
        },
    )
    return response


@router.post("/rooms/{room_id}/auto/start")
async def start_auto_game(
    room_id: str,
    request: AutoGameControlRequest,
    db: Session = Depends(get_db),
):
    room = RoomService.get_room_by_id(db, room_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    if room.host_token != request.host_token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid host token")
    if room.status != RoomStatus.PLAYING:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Game must be started before auto host can run")

    AutoGameOrchestrator.start_room(room.room_code)
    return {"message": "Auto host started", "room_code": room.room_code}


@router.post("/rooms/{room_id}/auto/pause")
async def pause_auto_game(room_id: str, request: AutoGameControlRequest, db: Session = Depends(get_db)):
    room = RoomService.get_room_by_id(db, room_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    if room.host_token != request.host_token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid host token")
    room.is_paused = True
    db.add(room)
    db.commit()
    db.refresh(room)
    await manager.broadcast_room(room.room_code, {"type": "GAME_PAUSED", "room_code": room.room_code, "payload": state_response(room).model_dump(mode="json"), "timestamp": now_iso()})
    return {"message": "Game paused"}


@router.post("/rooms/{room_id}/auto/resume")
async def resume_auto_game(room_id: str, request: AutoGameControlRequest, db: Session = Depends(get_db)):
    room = RoomService.get_room_by_id(db, room_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    if room.host_token != request.host_token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid host token")
    room.is_paused = False
    db.add(room)
    db.commit()
    db.refresh(room)
    await manager.broadcast_room(room.room_code, {"type": "GAME_RESUMED", "room_code": room.room_code, "payload": state_response(room).model_dump(mode="json"), "timestamp": now_iso()})
    return {"message": "Game resumed"}


@router.post("/rooms/{room_id}/auto/stop")
async def stop_auto_game(room_id: str, request: AutoGameControlRequest, db: Session = Depends(get_db)):
    room = RoomService.get_room_by_id(db, room_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    if room.host_token != request.host_token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid host token")
    AutoGameOrchestrator.stop_room(room.room_code)
    room.status = RoomStatus.ENDED
    room.current_phase = GamePhase.ENDED
    room.is_game_over = True
    room.current_audio_text = "Trò chơi đã được Host kết thúc."
    db.add(room)
    db.commit()
    db.refresh(room)
    await manager.broadcast_room(room.room_code, {"type": "GAME_OVER", "room_code": room.room_code, "payload": state_response(room).model_dump(mode="json"), "timestamp": now_iso()})
    return {"message": "Game stopped"}


@router.get("/rooms/{room_id}/state", response_model=GameStateResponse)
async def get_game_state(room_id: str, db: Session = Depends(get_db)):
    room = RoomService.get_room_by_id(db, room_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    return state_response(room)


@router.post("/rooms/{room_id}/night/action")
async def submit_night_action(room_id: str, request: NightActionRequest, db: Session = Depends(get_db)):
    room = RoomService.get_room_by_id(db, room_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    try:
        result = NightActionService.submit_action(
            db=db,
            room=room,
            player_id=request.player_id,
            session_token=request.session_token,
            action_type=request.action_type,
            target_player_id=request.target_player_id,
            target_player_ids=request.target_player_ids,
        )
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    await manager.send_to_host(
        room.room_code,
        {
            "type": "ACTION_RECEIVED",
            "room_code": room.room_code,
            "payload": {"player_id": request.player_id, "action_type": request.action_type},
            "timestamp": now_iso(),
        },
    )
    await manager.send_to_player(
        room.room_code,
        request.player_id,
        {
            "type": "ACTION_RECEIVED",
            "room_code": room.room_code,
            "payload": result,
            "timestamp": now_iso(),
        },
    )
    return result


@router.post("/rooms/{room_id}/vote")
async def submit_vote(room_id: str, request: VoteRequest, db: Session = Depends(get_db)):
    room = RoomService.get_room_by_id(db, room_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    try:
        summary = VoteService.submit_vote(
            db=db,
            room=room,
            voter_player_id=request.voter_player_id,
            session_token=request.session_token,
            target_player_id=request.target_player_id,
        )
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    await manager.broadcast_room(
        room.room_code,
        {
            "type": "VOTE_UPDATED",
            "room_code": room.room_code,
            "payload": summary,
            "timestamp": now_iso(),
        },
    )
    return summary


@router.get("/rooms/{room_id}/logs")
async def get_game_logs(
    room_id: str,
    host_token: str = Header(..., alias="X-Host-Token"),
    db: Session = Depends(get_db),
):
    room = RoomService.get_room_by_id(db, room_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    if room.host_token != host_token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid host token")
    if not room.is_game_over:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Logs are available after game over only")
    return {"logs": GameLogService.get_logs(db, room_id)}


@router.get("/players/{player_id}/role", response_model=PlayerRoleResponse)
async def get_my_role(
    player_id: str,
    session_token: str = Query(..., description="Player session token"),
    db: Session = Depends(get_db),
):
    try:
        role_info = GameStartService.get_player_role(db=db, player_id=player_id, session_token=session_token)
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        message = str(e)
        if "not found" in message.lower():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
    return PlayerRoleResponse(**role_info)
