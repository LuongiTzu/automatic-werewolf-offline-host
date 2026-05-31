"""Game log service."""
import json
import uuid
from typing import Any

from sqlalchemy.orm import Session

from app.models import GameLog, Room


class GameLogService:
    """Centralized game logging. Logs are mainly shown when the game ends."""

    @staticmethod
    def log(
        db: Session,
        room: Room,
        event_type: str,
        message: str,
        data: dict[str, Any] | None = None,
        night_number: int | None = None,
        day_number: int | None = None,
    ) -> GameLog:
        log = GameLog(
            id=str(uuid.uuid4()),
            room_id=room.id,
            night_number=room.night_number if night_number is None else night_number,
            day_number=room.day_number if day_number is None else day_number,
            event_type=event_type,
            message=message,
            data_json=json.dumps(data or {}, ensure_ascii=False),
        )
        db.add(log)
        db.commit()
        db.refresh(log)
        return log

    @staticmethod
    def get_logs(db: Session, room_id: str) -> list[dict[str, Any]]:
        logs = db.query(GameLog).filter(GameLog.room_id == room_id).order_by(GameLog.created_at.asc()).all()
        result: list[dict[str, Any]] = []
        for log in logs:
            try:
                data = json.loads(log.data_json or "{}")
            except json.JSONDecodeError:
                data = {}
            result.append(
                {
                    "id": log.id,
                    "night_number": log.night_number,
                    "day_number": log.day_number,
                    "event_type": log.event_type,
                    "message": log.message,
                    "data": data,
                    "created_at": log.created_at.isoformat() if log.created_at else None,
                }
            )
        return result
