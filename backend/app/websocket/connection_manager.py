"""WebSocket connection manager."""

import logging
from typing import Any

from fastapi import WebSocket

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manage WebSocket connections by room_code, host, and player id."""

    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}
        self.player_connections: dict[str, dict[str, list[WebSocket]]] = {}
        self.host_connections: dict[str, list[WebSocket]] = {}
        self.connection_meta: dict[WebSocket, dict[str, str | None]] = {}

    async def connect(
        self,
        room_code: str,
        websocket: WebSocket,
        client_type: str | None = None,
        client_id: str | None = None,
    ):
        """Accept and store a WebSocket connection for a room."""
        await websocket.accept()

        self.active_connections.setdefault(room_code, []).append(websocket)
        self.connection_meta[websocket] = {
            "room_code": room_code,
            "client_type": client_type,
            "client_id": client_id,
        }

        if client_type == "host":
            self.host_connections.setdefault(room_code, []).append(websocket)
        elif client_type == "player" and client_id:
            self.player_connections.setdefault(room_code, {}).setdefault(client_id, []).append(websocket)

        logger.info("WebSocket connected | room=%s | total=%s", room_code, len(self.active_connections[room_code]))

    def disconnect(self, room_code: str, websocket: WebSocket):
        """Remove a WebSocket connection from a room."""
        if room_code in self.active_connections and websocket in self.active_connections[room_code]:
            self.active_connections[room_code].remove(websocket)
            if not self.active_connections[room_code]:
                del self.active_connections[room_code]

        meta = self.connection_meta.pop(websocket, {})
        client_type = meta.get("client_type")
        client_id = meta.get("client_id")

        if client_type == "host" and room_code in self.host_connections:
            if websocket in self.host_connections[room_code]:
                self.host_connections[room_code].remove(websocket)
            if not self.host_connections[room_code]:
                del self.host_connections[room_code]

        if client_type == "player" and client_id and room_code in self.player_connections:
            player_map = self.player_connections[room_code]
            if client_id in player_map and websocket in player_map[client_id]:
                player_map[client_id].remove(websocket)
            if client_id in player_map and not player_map[client_id]:
                del player_map[client_id]
            if not player_map:
                del self.player_connections[room_code]

        logger.info("WebSocket disconnected | room=%s", room_code)

    async def send_personal_message(self, websocket: WebSocket, message: dict[str, Any]):
        """Send message to one WebSocket client."""
        await websocket.send_json(message)

    async def _send_many(self, websockets: list[WebSocket], room_code: str, message: dict[str, Any]):
        disconnected: list[WebSocket] = []
        for websocket in list(websockets):
            try:
                await websocket.send_json(message)
            except Exception as e:
                logger.warning("Failed to send WebSocket message: %s", e)
                disconnected.append(websocket)
        for websocket in disconnected:
            self.disconnect(room_code, websocket)

    async def broadcast_room(self, room_code: str, message: dict[str, Any]):
        """Broadcast message to all clients in a room."""
        connections = self.active_connections.get(room_code, [])
        if not connections:
            logger.info("No active WebSocket clients in room=%s", room_code)
            return
        await self._send_many(connections, room_code, message)

    async def send_to_player(self, room_code: str, player_id: str, message: dict[str, Any]):
        """Send a private event to a player only."""
        connections = self.player_connections.get(room_code, {}).get(player_id, [])
        if connections:
            await self._send_many(connections, room_code, message)

    async def send_to_host(self, room_code: str, message: dict[str, Any]):
        """Send an event to host connections only."""
        connections = self.host_connections.get(room_code, [])
        if connections:
            await self._send_many(connections, room_code, message)

    def get_connection_count(self, room_code: str) -> int:
        """Get number of active WebSocket connections in a room."""
        return len(self.active_connections.get(room_code, []))


manager = ConnectionManager()
