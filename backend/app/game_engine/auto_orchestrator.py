"""Automatic host/game orchestrator."""
import asyncio
from datetime import datetime, timedelta, timezone
from typing import Any

from app.database import SessionLocal
from app.game_engine.constants import (
    AUTO_TASK_DAY_RESULT_SECONDS,
    AUTO_TASK_DISCUSSION_SECONDS,
    AUTO_TASK_NIGHT_RESOLVE_SECONDS,
    AUTO_TASK_NIGHT_START_SECONDS,
    AUTO_TASK_ROLE_REVEAL_SECONDS,
    AUTO_TASK_VOTE_RESULT_SECONDS,
    AUTO_TASK_VOTING_SECONDS,
)
from app.game_engine.night_resolver import NightResolver
from app.game_engine.role_rules import get_existing_alive_night_roles, get_role_audio_text, get_role_sleep_text, get_role_turn_seconds
from app.game_engine.vote_resolver import VoteResolver
from app.game_engine.win_condition import WinCondition
from app.models import GamePhase, Player, Room, RoomStatus
from app.services.game_log_service import GameLogService
from app.websocket.connection_manager import manager


def utcnow() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def enum_value(value: Any) -> Any:
    return value.value if hasattr(value, "value") else value


class AutoGameOrchestrator:
    """Runs the whole Werewolf MVP flow after Host starts the automatic game."""

    _tasks: dict[str, asyncio.Task] = {}

    @classmethod
    def is_running(cls, room_code: str) -> bool:
        task = cls._tasks.get(room_code)
        return bool(task and not task.done())

    @classmethod
    def start_room(cls, room_code: str):
        if cls.is_running(room_code):
            return
        cls._tasks[room_code] = asyncio.create_task(cls._run_room(room_code))

    @classmethod
    def stop_room(cls, room_code: str):
        task = cls._tasks.get(room_code)
        if task and not task.done():
            task.cancel()

    @classmethod
    async def _broadcast_phase(cls, room: Room, extra_payload: dict | None = None):
        payload = {
            "room_id": room.id,
            "room_code": room.room_code,
            "status": enum_value(room.status),
            "current_phase": enum_value(room.current_phase),
            "night_number": room.night_number,
            "day_number": room.day_number,
            "current_role_turn": room.current_role_turn,
            "phase_ends_at": room.phase_ends_at.isoformat() if room.phase_ends_at else None,
            "current_audio_text": room.current_audio_text,
            "is_paused": room.is_paused,
            "is_game_over": room.is_game_over,
            "winner": room.winner,
        }
        if extra_payload:
            payload.update(extra_payload)
        await manager.broadcast_room(
            room.room_code,
            {
                "type": "PHASE_CHANGED",
                "room_code": room.room_code,
                "payload": payload,
                "timestamp": iso_now(),
            },
        )

    @classmethod
    async def _set_phase(cls, db, room: Room, phase: GamePhase, seconds: int, audio_text: str, role_code: str | None = None):
        room.current_phase = phase
        room.current_role_turn = role_code
        room.current_audio_text = audio_text
        room.phase_ends_at = utcnow() + timedelta(seconds=seconds) if seconds > 0 else None
        db.add(room)
        db.commit()
        db.refresh(room)
        await cls._broadcast_phase(room)

    @classmethod
    async def _sleep_with_pause(cls, room_code: str, seconds: int):
        for _ in range(max(seconds, 0)):
            await asyncio.sleep(1)
            db = SessionLocal()
            try:
                room = db.query(Room).filter(Room.room_code == room_code).first()
                if not room or room.is_game_over or room.status == RoomStatus.ENDED:
                    return
                while room.is_paused:
                    await asyncio.sleep(1)
                    db.refresh(room)
            finally:
                db.close()

    @classmethod
    async def _run_room(cls, room_code: str):
        try:
            db = SessionLocal()
            try:
                room = db.query(Room).filter(Room.room_code == room_code).first()
                if not room or room.status != RoomStatus.PLAYING:
                    return
                await cls._set_phase(
                    db,
                    room,
                    GamePhase.ROLE_REVEAL,
                    AUTO_TASK_ROLE_REVEAL_SECONDS,
                    "Mỗi người chơi hãy xem vai trò của mình và ghi nhớ nhiệm vụ.",
                )
            finally:
                db.close()

            await cls._sleep_with_pause(room_code, AUTO_TASK_ROLE_REVEAL_SECONDS)

            while True:
                db = SessionLocal()
                try:
                    room = db.query(Room).filter(Room.room_code == room_code).first()
                    if not room or room.is_game_over or room.status == RoomStatus.ENDED:
                        return

                    room.night_number += 1
                    room.current_phase = GamePhase.NIGHT_START
                    room.current_role_turn = None
                    room.current_audio_text = "Trời tối rồi. Tất cả người chơi hãy nhắm mắt lại. Đêm nay bắt đầu."
                    room.phase_ends_at = utcnow() + timedelta(seconds=AUTO_TASK_NIGHT_START_SECONDS)
                    db.add(room)
                    db.commit()
                    db.refresh(room)
                    GameLogService.log(db, room, "NIGHT_STARTED", f"Night {room.night_number} started")
                    await cls._broadcast_phase(room)
                finally:
                    db.close()

                await cls._sleep_with_pause(room_code, AUTO_TASK_NIGHT_START_SECONDS)

                db = SessionLocal()
                try:
                    room = db.query(Room).filter(Room.room_code == room_code).first()
                    if not room or room.is_game_over:
                        return
                    players = db.query(Player).filter(Player.room_id == room.id).all()
                    role_order = get_existing_alive_night_roles(players)
                finally:
                    db.close()

                for role_code in role_order:
                    db = SessionLocal()
                    try:
                        room = db.query(Room).filter(Room.room_code == room_code).first()
                        if not room or room.is_game_over:
                            return
                        seconds = get_role_turn_seconds(role_code)
                        audio_text = get_role_audio_text(role_code)
                        await cls._set_phase(db, room, GamePhase.NIGHT_ROLE_TURN, seconds, audio_text, role_code=role_code)

                        allowed_players = db.query(Player).filter(
                            Player.room_id == room.id,
                            Player.role_code == role_code,
                            Player.is_alive.is_(True),
                        ).all()
                        public_players = db.query(Player).filter(Player.room_id == room.id).all()
                        target_list = [
                            {"id": p.id, "name": p.name, "is_alive": p.is_alive}
                            for p in public_players
                            if p.is_alive
                        ]
                        for player in allowed_players:
                            await manager.send_to_player(
                                room.room_code,
                                player.id,
                                {
                                    "type": "PLAYER_WAKE_ALLOWED",
                                    "room_code": room.room_code,
                                    "payload": {
                                        "role_code": role_code,
                                        "night_number": room.night_number,
                                        "phase_ends_at": room.phase_ends_at.isoformat() if room.phase_ends_at else None,
                                        "targets": target_list,
                                    },
                                    "timestamp": iso_now(),
                                },
                            )
                    finally:
                        db.close()

                    await cls._sleep_with_pause(room_code, get_role_turn_seconds(role_code))

                    db = SessionLocal()
                    try:
                        room = db.query(Room).filter(Room.room_code == room_code).first()
                        if not room or room.is_game_over:
                            return
                        sleep_text = get_role_sleep_text(role_code)
                        room.current_audio_text = sleep_text
                        db.add(room)
                        db.commit()
                        await manager.broadcast_room(
                            room.room_code,
                            {
                                "type": "PLAYER_SLEEP",
                                "room_code": room.room_code,
                                "payload": {"role_code": role_code, "audio_text": sleep_text},
                                "timestamp": iso_now(),
                            },
                        )
                    finally:
                        db.close()

                db = SessionLocal()
                try:
                    room = db.query(Room).filter(Room.room_code == room_code).first()
                    if not room or room.is_game_over:
                        return
                    await cls._set_phase(
                        db,
                        room,
                        GamePhase.NIGHT_RESOLVING,
                        AUTO_TASK_NIGHT_RESOLVE_SECONDS,
                        "Tất cả người chơi tiếp tục nhắm mắt. Hệ thống đang xử lý kết quả trong đêm.",
                    )
                    night_result = NightResolver.resolve_night(db, room)
                    winner = WinCondition.apply_game_over_if_needed(db, room)
                    if winner:
                        await manager.broadcast_room(
                            room.room_code,
                            {
                                "type": "GAME_OVER",
                                "room_code": room.room_code,
                                "payload": {"winner": winner, "audio_text": room.current_audio_text},
                                "timestamp": iso_now(),
                            },
                        )
                        return
                finally:
                    db.close()

                await cls._sleep_with_pause(room_code, AUTO_TASK_NIGHT_RESOLVE_SECONDS)

                db = SessionLocal()
                try:
                    room = db.query(Room).filter(Room.room_code == room_code).first()
                    if not room or room.is_game_over:
                        return
                    room.day_number += 1
                    dead_names = [p["name"] for p in night_result.get("dead_players", [])]
                    result_text = "Đêm qua không có ai chết." if not dead_names else f"Đêm qua, người chơi sau đã chết: {', '.join(dead_names)}."
                    await cls._set_phase(
                        db,
                        room,
                        GamePhase.DAY_RESULT,
                        AUTO_TASK_DAY_RESULT_SECONDS,
                        f"Trời sáng rồi. Tất cả người chơi hãy mở mắt. {result_text}",
                    )
                    await manager.broadcast_room(
                        room.room_code,
                        {
                            "type": "DAY_STARTED",
                            "room_code": room.room_code,
                            "payload": {"day_number": room.day_number, "dead_players": night_result.get("dead_players", [])},
                            "timestamp": iso_now(),
                        },
                    )
                finally:
                    db.close()

                await cls._sleep_with_pause(room_code, AUTO_TASK_DAY_RESULT_SECONDS)

                db = SessionLocal()
                try:
                    room = db.query(Room).filter(Room.room_code == room_code).first()
                    if not room or room.is_game_over:
                        return
                    await cls._set_phase(
                        db,
                        room,
                        GamePhase.DAY_DISCUSSION,
                        AUTO_TASK_DISCUSSION_SECONDS,
                        "Thời gian thảo luận bắt đầu.",
                    )
                    await manager.broadcast_room(
                        room.room_code,
                        {
                            "type": "DISCUSSION_STARTED",
                            "room_code": room.room_code,
                            "payload": {"day_number": room.day_number, "seconds": AUTO_TASK_DISCUSSION_SECONDS},
                            "timestamp": iso_now(),
                        },
                    )
                finally:
                    db.close()

                await cls._sleep_with_pause(room_code, AUTO_TASK_DISCUSSION_SECONDS)

                db = SessionLocal()
                try:
                    room = db.query(Room).filter(Room.room_code == room_code).first()
                    if not room or room.is_game_over:
                        return
                    await cls._set_phase(
                        db,
                        room,
                        GamePhase.VOTING,
                        AUTO_TASK_VOTING_SECONDS,
                        "Thời gian thảo luận đã kết thúc. Bắt đầu bỏ phiếu treo cổ.",
                    )
                    alive_players = db.query(Player).filter(Player.room_id == room.id, Player.is_alive.is_(True)).all()
                    await manager.broadcast_room(
                        room.room_code,
                        {
                            "type": "VOTE_STARTED",
                            "room_code": room.room_code,
                            "payload": {
                                "day_number": room.day_number,
                                "seconds": AUTO_TASK_VOTING_SECONDS,
                                "targets": [{"id": p.id, "name": p.name} for p in alive_players],
                            },
                            "timestamp": iso_now(),
                        },
                    )
                finally:
                    db.close()

                await cls._sleep_with_pause(room_code, AUTO_TASK_VOTING_SECONDS)

                db = SessionLocal()
                try:
                    room = db.query(Room).filter(Room.room_code == room_code).first()
                    if not room or room.is_game_over:
                        return
                    vote_result = VoteResolver.resolve_vote(db, room)
                    await cls._set_phase(
                        db,
                        room,
                        GamePhase.VOTE_RESULT,
                        AUTO_TASK_VOTE_RESULT_SECONDS,
                        vote_result["message"],
                    )
                    await manager.broadcast_room(
                        room.room_code,
                        {
                            "type": "VOTE_ENDED",
                            "room_code": room.room_code,
                            "payload": vote_result,
                            "timestamp": iso_now(),
                        },
                    )
                    winner = WinCondition.apply_game_over_if_needed(db, room)
                    if winner:
                        await manager.broadcast_room(
                            room.room_code,
                            {
                                "type": "GAME_OVER",
                                "room_code": room.room_code,
                                "payload": {"winner": winner, "audio_text": room.current_audio_text},
                                "timestamp": iso_now(),
                            },
                        )
                        return
                finally:
                    db.close()

                await cls._sleep_with_pause(room_code, AUTO_TASK_VOTE_RESULT_SECONDS)
        except asyncio.CancelledError:
            return
        finally:
            cls._tasks.pop(room_code, None)
