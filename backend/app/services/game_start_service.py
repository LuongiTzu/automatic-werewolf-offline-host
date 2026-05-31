"""Game start service."""
import random
import uuid
from sqlalchemy.orm import Session

from app.models import Player, PlayerStatusEffect, Role, Room, RoomRoleCart, RoomStatus, GamePhase, WitchState
from app.services.game_log_service import GameLogService
from app.services.room_service import RoomService


class GameStartService:
    """Business logic for starting a game and assigning roles."""

    @staticmethod
    def _build_role_pool(cart_items: list[RoomRoleCart]) -> list[str]:
        role_pool: list[str] = []
        for item in cart_items:
            if item.quantity > 0:
                role_pool.extend([item.role_code] * item.quantity)
        return role_pool

    @staticmethod
    def _select_roles_for_players(role_pool: list[str], player_count: int) -> list[str]:
        if player_count <= 0:
            raise ValueError("At least one player is required to start the game")
        if len(role_pool) < player_count:
            raise ValueError("Not enough roles for players")
        if "WEREWOLF" not in role_pool:
            raise ValueError("At least one WEREWOLF role is required")

        for _ in range(100):
            selected_roles = random.sample(role_pool, player_count)
            if "WEREWOLF" in selected_roles:
                return selected_roles

        selected_roles = random.sample(role_pool, player_count)
        if "WEREWOLF" not in selected_roles:
            selected_roles[0] = "WEREWOLF"
        random.shuffle(selected_roles)
        return selected_roles

    @staticmethod
    def start_game(db: Session, room_code: str) -> Room:
        room = RoomService.get_room_by_code(db, room_code)
        if not room:
            raise ValueError(f"Room with code '{room_code}' not found")
        if room.status != RoomStatus.WAITING:
            raise ValueError("Room has already started or ended")

        players = RoomService.get_room_players(db, room.id)
        if len(players) == 0:
            raise ValueError("At least one player is required to start the game")

        cart_items = db.query(RoomRoleCart).filter(RoomRoleCart.room_id == room.id).all()
        role_pool = GameStartService._build_role_pool(cart_items)
        if len(role_pool) < len(players):
            raise ValueError("Total roles must be greater than or equal to total players")
        if "WEREWOLF" not in role_pool:
            raise ValueError("Role cart must include at least one WEREWOLF")

        selected_roles = GameStartService._select_roles_for_players(role_pool, len(players))
        shuffled_players = players[:]
        random.shuffle(shuffled_players)

        role_map = {role.code: role for role in db.query(Role).all()}
        assigned_log = []
        for player, role_code in zip(shuffled_players, selected_roles):
            role = role_map.get(role_code)
            player.role_code = role_code
            player.side = role.side.value if role and hasattr(role.side, "value") else (str(role.side) if role else None)
            player.is_alive = True
            player.is_ready = False
            db.add(player)
            assigned_log.append({"player_id": player.id, "player_name": player.name, "role_code": role_code})

            status_exists = db.query(PlayerStatusEffect).filter(
                PlayerStatusEffect.room_id == room.id,
                PlayerStatusEffect.player_id == player.id,
            ).first()
            if not status_exists:
                db.add(PlayerStatusEffect(id=str(uuid.uuid4()), room_id=room.id, player_id=player.id))

            if role_code == "WITCH":
                witch_exists = db.query(WitchState).filter(
                    WitchState.room_id == room.id,
                    WitchState.player_id == player.id,
                ).first()
                if not witch_exists:
                    db.add(WitchState(id=str(uuid.uuid4()), room_id=room.id, player_id=player.id))

        room.status = RoomStatus.PLAYING
        room.current_phase = GamePhase.ROLE_REVEAL
        room.night_number = 0
        room.day_number = 0
        room.current_role_turn = None
        room.phase_ends_at = None
        room.current_audio_text = "Mỗi người chơi hãy xem vai trò của mình và ghi nhớ nhiệm vụ."
        room.is_paused = False
        room.is_game_over = False
        room.winner = None

        db.add(room)
        db.commit()
        db.refresh(room)

        GameLogService.log(
            db,
            room,
            event_type="ROLES_ASSIGNED",
            message="Roles assigned to players",
            data={"assignments": assigned_log},
            night_number=0,
            day_number=0,
        )
        return room

    @staticmethod
    def get_player_role(db: Session, player_id: str, session_token: str) -> dict:
        player = db.query(Player).filter(Player.id == player_id).first()
        if not player:
            raise ValueError("Player not found")
        if player.session_token != session_token:
            raise PermissionError("Invalid session token")
        if not player.role_code:
            raise ValueError("Game has not started or role has not been assigned yet")

        role = db.query(Role).filter(Role.code == player.role_code).first()
        if not role:
            raise ValueError("Assigned role does not exist")

        return {
            "player_id": player.id,
            "player_name": player.name,
            "room_id": player.room_id,
            "role_code": role.code,
            "role_name": role.name,
            "side": role.side.value if hasattr(role.side, "value") else str(role.side),
            "description": role.description,
            "night_order": role.night_order,
        }
