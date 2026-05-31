"""WebSocket connection manager"""

import logging
from typing import Any

from fastapi import WebSocket

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manage WebSocket connections by room_code."""

    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, room_code: str, websocket: WebSocket):
        """Accept and store a WebSocket connection for a room."""
        await websocket.accept()

        if room_code not in self.active_connections:
            self.active_connections[room_code] = []

        self.active_connections[room_code].append(websocket)

        logger.info(
            "WebSocket connected | room=%s | total=%s",
            room_code,
            len(self.active_connections[room_code]),
        )

    def disconnect(self, room_code: str, websocket: WebSocket):
        """Remove a WebSocket connection from a room."""
        if room_code not in self.active_connections:
            return

        if websocket in self.active_connections[room_code]:
            self.active_connections[room_code].remove(websocket)

        if len(self.active_connections[room_code]) == 0:
            del self.active_connections[room_code]

        logger.info("WebSocket disconnected | room=%s", room_code)

    async def send_personal_message(self, websocket: WebSocket, message: dict[str, Any]):
        """Send message to one WebSocket client."""
        await websocket.send_json(message)

    async def broadcast_room(self, room_code: str, message: dict[str, Any]):
        """Broadcast message to all clients in a room."""
        connections = self.active_connections.get(room_code, [])

        if not connections:
            logger.info("No active WebSocket clients in room=%s", room_code)
            return

        disconnected: list[WebSocket] = []

        for websocket in connections:
            try:
                await websocket.send_json(message)
            except Exception as e:
                logger.warning("Failed to send WebSocket message: %s", e)
                disconnected.append(websocket)

        for websocket in disconnected:
            self.disconnect(room_code, websocket)

    def get_connection_count(self, room_code: str) -> int:
        """Get number of active WebSocket connections in a room."""
        return len(self.active_connections.get(room_code, []))


manager = ConnectionManager()