"""WebSocket routers."""
import json
from datetime import datetime, timezone

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.database import SessionLocal
from app.services import PlayerService, RoomService
from app.websocket.connection_manager import manager

router = APIRouter(tags=["websocket"])


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@router.websocket("/ws/rooms/{room_code}")
async def room_websocket(
    websocket: WebSocket,
    room_code: str,
    client_type: str = "player",
    client_id: str | None = None,
):
    db = SessionLocal()
    try:
        room = RoomService.get_room_by_code(db, room_code)
        if room and client_type == "player" and client_id:
            PlayerService.update_player_connection(db, client_id, True)
    finally:
        db.close()

    if not room:
        await websocket.close(code=1008)
        return

    await manager.connect(room_code, websocket, client_type=client_type, client_id=client_id)
    await manager.send_personal_message(
        websocket,
        {
            "type": "CONNECTION_ESTABLISHED",
            "room_code": room_code,
            "payload": {
                "message": "Connected to room WebSocket",
                "client_type": client_type,
                "client_id": client_id,
                "connection_count": manager.get_connection_count(room_code),
            },
            "timestamp": now_iso(),
        },
    )

    try:
        while True:
            raw_message = await websocket.receive_text()
            try:
                event = json.loads(raw_message)
            except json.JSONDecodeError:
                await manager.send_personal_message(websocket, {"type": "ERROR_MESSAGE", "room_code": room_code, "payload": {"message": "Invalid JSON message"}, "timestamp": now_iso()})
                continue

            event_type = event.get("type")
            if event_type == "PING":
                await manager.send_personal_message(websocket, {"type": "PONG", "room_code": room_code, "payload": {"message": "pong"}, "timestamp": now_iso()})
            elif event_type == "CLIENT_READY":
                await manager.broadcast_room(room_code, {"type": "CLIENT_READY", "room_code": room_code, "payload": {"client_type": client_type, "client_id": client_id}, "timestamp": now_iso()})
            else:
                await manager.send_personal_message(websocket, {"type": "INFO_MESSAGE", "room_code": room_code, "payload": {"message": f"Event '{event_type}' received. Use REST APIs for game actions in this backend version."}, "timestamp": now_iso()})

    except WebSocketDisconnect:
        manager.disconnect(room_code, websocket)
        db = SessionLocal()
        try:
            if client_type == "player" and client_id:
                PlayerService.update_player_connection(db, client_id, False)
        finally:
            db.close()
        await manager.broadcast_room(room_code, {"type": "CLIENT_DISCONNECTED", "room_code": room_code, "payload": {"client_type": client_type, "client_id": client_id, "connection_count": manager.get_connection_count(room_code)}, "timestamp": now_iso()})
    except Exception:
        manager.disconnect(room_code, websocket)
        try:
            await websocket.close(code=1011)
        except Exception:
            pass
