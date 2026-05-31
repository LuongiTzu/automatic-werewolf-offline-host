"""Night action service."""
import json
import uuid
from typing import Any

from sqlalchemy.orm import Session

from app.game_engine.constants import (
    ACTION_GUARD_PROTECT,
    ACTION_SEER_CHECK,
    ACTION_SKIP,
    ACTION_WEREWOLF_BITE,
    ACTION_WITCH_HEAL,
    ACTION_WITCH_POISON,
    ROLE_GUARD,
    ROLE_SEER,
    ROLE_WEREWOLF,
    ROLE_WITCH,
)
from app.models import GamePhase, NightAction, Player, Room, WitchState
from app.services.game_log_service import GameLogService


class NightActionService:
    """Validate and store night actions."""

    ROLE_ALLOWED_ACTIONS = {
        ROLE_GUARD: {ACTION_GUARD_PROTECT},
        ROLE_WEREWOLF: {ACTION_WEREWOLF_BITE},
        ROLE_SEER: {ACTION_SEER_CHECK},
        ROLE_WITCH: {ACTION_WITCH_HEAL, ACTION_WITCH_POISON, ACTION_SKIP},
    }

    @staticmethod
    def submit_action(
        db: Session,
        room: Room,
        player_id: str,
        session_token: str,
        action_type: str,
        target_player_id: str | None = None,
        target_player_ids: list[str] | None = None,
    ) -> dict[str, Any]:
        if room.current_phase != GamePhase.NIGHT_ROLE_TURN:
            raise ValueError("Night action is only allowed during a night role turn")

        player = db.query(Player).filter(Player.id == player_id, Player.room_id == room.id).first()
        if not player:
            raise ValueError("Player not found in this room")
        if player.session_token != session_token:
            raise PermissionError("Invalid session token")
        if not player.is_alive:
            raise ValueError("Dead players cannot submit night actions")
        if player.role_code != room.current_role_turn:
            raise ValueError("It is not this player's role turn")

        allowed = NightActionService.ROLE_ALLOWED_ACTIONS.get(player.role_code or "", set())
        if action_type not in allowed:
            raise ValueError("This action is not allowed for the current role")

        target = None
        if target_player_id:
            target = db.query(Player).filter(Player.id == target_player_id, Player.room_id == room.id).first()
            if not target:
                raise ValueError("Target player not found in this room")
            if not target.is_alive:
                raise ValueError("Target player is not alive")

        if action_type == ACTION_WEREWOLF_BITE:
            if not target:
                raise ValueError("Werewolf must choose a target")
            if target.role_code == ROLE_WEREWOLF:
                raise ValueError("Werewolf cannot bite another normal werewolf")

        if action_type == ACTION_GUARD_PROTECT and not target:
            raise ValueError("Guard must choose one target")

        if action_type == ACTION_SEER_CHECK and not target:
            raise ValueError("Seer must choose one target")

        if action_type in {ACTION_WITCH_HEAL, ACTION_WITCH_POISON}:
            witch_state = db.query(WitchState).filter(
                WitchState.room_id == room.id,
                WitchState.player_id == player.id,
            ).first()
            if not witch_state:
                witch_state = WitchState(
                    id=str(uuid.uuid4()),
                    room_id=room.id,
                    player_id=player.id,
                    healing_potion_available=True,
                    poison_potion_available=True,
                )
                db.add(witch_state)
                db.commit()
                db.refresh(witch_state)

            if action_type == ACTION_WITCH_HEAL and not witch_state.healing_potion_available:
                raise ValueError("Healing potion has already been used")
            if action_type == ACTION_WITCH_POISON:
                if not witch_state.poison_potion_available:
                    raise ValueError("Poison potion has already been used")
                if not target:
                    raise ValueError("Witch poison requires one target")

        existing = db.query(NightAction).filter(
            NightAction.room_id == room.id,
            NightAction.night_number == room.night_number,
            NightAction.actor_player_id == player.id,
            NightAction.action_type == action_type,
        ).first()

        if existing:
            existing.target_player_id = target_player_id
            existing.target_player_ids = json.dumps(target_player_ids or [], ensure_ascii=False)
            action = existing
        else:
            action = NightAction(
                id=str(uuid.uuid4()),
                room_id=room.id,
                night_number=room.night_number,
                actor_player_id=player.id,
                actor_role_code=player.role_code or "",
                action_type=action_type,
                target_player_id=target_player_id,
                target_player_ids=json.dumps(target_player_ids or [], ensure_ascii=False),
            )
            db.add(action)

        private_result = None
        if action_type == ACTION_SEER_CHECK and target:
            private_result = {
                "target_player_id": target.id,
                "target_name": target.name,
                "result": "Sói" if target.role_code == ROLE_WEREWOLF or target.side == "werewolf" else "Không phải Sói",
            }

        GameLogService.log(
            db,
            room,
            event_type="NIGHT_ACTION",
            message=f"{player.name} submitted {action_type}",
            data={
                "actor_player_id": player.id,
                "actor_name": player.name,
                "actor_role_code": player.role_code,
                "action_type": action_type,
                "target_player_id": target_player_id,
                "target_name": target.name if target else None,
            },
        )

        db.commit()
        db.refresh(action)
        return {
            "action_id": action.id,
            "action_type": action.action_type,
            "actor_player_id": player.id,
            "private_result": private_result,
        }

    @staticmethod
    def count_submitted_for_current_role(db: Session, room: Room) -> int:
        if not room.current_role_turn:
            return 0
        return db.query(NightAction).filter(
            NightAction.room_id == room.id,
            NightAction.night_number == room.night_number,
            NightAction.actor_role_code == room.current_role_turn,
        ).count()

    @staticmethod
    def count_alive_actors_for_current_role(db: Session, room: Room) -> int:
        if not room.current_role_turn:
            return 0
        return db.query(Player).filter(
            Player.room_id == room.id,
            Player.role_code == room.current_role_turn,
            Player.is_alive.is_(True),
        ).count()
