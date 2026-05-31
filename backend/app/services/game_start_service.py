"""Game start service.

This service handles starting a game and assigning roles to players.
Backend is the single source of truth:
- Clients never assign roles.
- Clients never decide game state.
- Server validates room, player count, role cart, and role assignment.
"""

import random
from sqlalchemy.orm import Session

from app.models import Room, Player, Role, RoomRoleCart, RoomStatus, GamePhase
from app.services.room_service import RoomService


class GameStartService:
    """Business logic for starting a game."""

    @staticmethod
    def _build_role_pool(cart_items: list[RoomRoleCart]) -> list[str]:
        """Build a flat role pool from role cart items.

        Example:
        WEREWOLF x 1, VILLAGER x 3
        -> ["WEREWOLF", "VILLAGER", "VILLAGER", "VILLAGER"]
        """
        role_pool: list[str] = []

        for item in cart_items:
            if item.quantity > 0:
                role_pool.extend([item.role_code] * item.quantity)

        return role_pool

    @staticmethod
    def _select_roles_for_players(role_pool: list[str], player_count: int) -> list[str]:
        """Randomly select roles for players.

        Requirement:
        - Number of selected roles must equal number of players.
        - Selected roles must contain at least 1 WEREWOLF.
        """
        if player_count <= 0:
            raise ValueError("At least one player is required to start the game")

        if len(role_pool) < player_count:
            raise ValueError("Not enough roles for players")

        if "WEREWOLF" not in role_pool:
            raise ValueError("At least one WEREWOLF role is required")

        max_retry = 100

        for _ in range(max_retry):
            selected_roles = random.sample(role_pool, player_count)

            if "WEREWOLF" in selected_roles:
                return selected_roles

        # Fallback: this should rarely happen, but avoids random failure.
        selected_roles = random.sample(role_pool, player_count)

        if "WEREWOLF" not in selected_roles:
            selected_roles[0] = "WEREWOLF"

        random.shuffle(selected_roles)
        return selected_roles

    @staticmethod
    def start_game(db: Session, room_code: str) -> Room:
        """Start game and assign roles to players.

        Validations:
        - Room exists.
        - Room is still waiting.
        - At least 1 player exists.
        - Total selected roles >= player count.
        - Role cart includes at least 1 WEREWOLF.
        """
        room = RoomService.get_room_by_code(db, room_code)

        if not room:
            raise ValueError(f"Room with code '{room_code}' not found")

        if room.status != RoomStatus.WAITING:
            raise ValueError("Room has already started or ended")

        players = RoomService.get_room_players(db, room.id)

        if len(players) == 0:
            raise ValueError("At least one player is required to start the game")

        cart_items = db.query(RoomRoleCart).filter(
            RoomRoleCart.room_id == room.id
        ).all()

        role_pool = GameStartService._build_role_pool(cart_items)

        if len(role_pool) < len(players):
            raise ValueError("Total roles must be greater than or equal to total players")

        if "WEREWOLF" not in role_pool:
            raise ValueError("Role cart must include at least one WEREWOLF")

        selected_roles = GameStartService._select_roles_for_players(
            role_pool=role_pool,
            player_count=len(players),
        )

        shuffled_players = players[:]
        random.shuffle(shuffled_players)

        for player, role_code in zip(shuffled_players, selected_roles):
            player.role_code = role_code
            player.is_alive = True
            db.add(player)

        room.status = RoomStatus.PLAYING
        room.current_phase = GamePhase.NIGHT
        room.night_number = 1
        room.day_number = 0

        db.add(room)
        db.commit()
        db.refresh(room)

        return room

    @staticmethod
    def get_player_role(
        db: Session,
        player_id: str,
        session_token: str,
    ) -> dict:
        """Get role information for one player.

        Security:
        - A player can only get their own role.
        - session_token must match the player_id.
        """
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