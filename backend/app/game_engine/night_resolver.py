"""Night resolver for MVP roles."""
import random
from collections import Counter
from sqlalchemy.orm import Session

from app.game_engine.constants import (
    ACTION_GUARD_PROTECT,
    ACTION_WEREWOLF_BITE,
    ACTION_WITCH_HEAL,
    ACTION_WITCH_POISON,
)
from app.models import NightAction, Player, Room, WitchState
from app.services.game_log_service import GameLogService


class NightResolver:
    """Resolve the official death list after all night turns."""

    @staticmethod
    def _get_most_voted_target(actions: list[NightAction]) -> str | None:
        targets = [a.target_player_id for a in actions if a.target_player_id]
        if not targets:
            return None
        counts = Counter(targets)
        max_votes = max(counts.values())
        tied = [target for target, count in counts.items() if count == max_votes]
        return random.choice(tied)

    @staticmethod
    def resolve_night(db: Session, room: Room) -> dict:
        actions = db.query(NightAction).filter(
            NightAction.room_id == room.id,
            NightAction.night_number == room.night_number,
        ).all()

        bite_actions = [a for a in actions if a.action_type == ACTION_WEREWOLF_BITE]
        guard_actions = [a for a in actions if a.action_type == ACTION_GUARD_PROTECT]
        heal_actions = [a for a in actions if a.action_type == ACTION_WITCH_HEAL]
        poison_actions = [a for a in actions if a.action_type == ACTION_WITCH_POISON]

        bitten_player_id = NightResolver._get_most_voted_target(bite_actions)
        protected_ids = {a.target_player_id for a in guard_actions if a.target_player_id}
        healed = bool(heal_actions)

        dead_ids: set[str] = set()
        if bitten_player_id and bitten_player_id not in protected_ids and not healed:
            dead_ids.add(bitten_player_id)

        for action in poison_actions:
            if action.target_player_id:
                dead_ids.add(action.target_player_id)

        # Consume witch potions only during resolve.
        if heal_actions or poison_actions:
            witch_player_ids = {a.actor_player_id for a in heal_actions + poison_actions}
            for witch_id in witch_player_ids:
                witch_state = db.query(WitchState).filter(
                    WitchState.room_id == room.id,
                    WitchState.player_id == witch_id,
                ).first()
                if not witch_state:
                    continue
                if any(a.actor_player_id == witch_id for a in heal_actions):
                    witch_state.healing_potion_available = False
                if any(a.actor_player_id == witch_id for a in poison_actions):
                    witch_state.poison_potion_available = False
                db.add(witch_state)

        dead_players: list[Player] = []
        if dead_ids:
            dead_players = db.query(Player).filter(
                Player.room_id == room.id,
                Player.id.in_(dead_ids),
                Player.is_alive.is_(True),
            ).all()
            for player in dead_players:
                player.is_alive = False
                db.add(player)

        db.commit()

        death_summary = [
            {"id": player.id, "name": player.name}
            for player in dead_players
        ]

        GameLogService.log(
            db,
            room,
            event_type="NIGHT_RESOLVED",
            message="Night resolved",
            data={
                "bitten_player_id": bitten_player_id,
                "protected_player_ids": list(protected_ids),
                "healed": healed,
                "dead_players": death_summary,
            },
        )

        return {
            "night_number": room.night_number,
            "dead_players": death_summary,
        }
