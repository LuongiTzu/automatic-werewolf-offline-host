"""Player service."""
import uuid
from sqlalchemy.orm import Session

from app.models import Player, RoomStatus
from app.services.room_service import RoomService


class PlayerService:
    """Player business logic service."""

    @staticmethod
    def join_room(db: Session, room_id: str, player_name: str) -> Player:
        """Create a new player and join a room."""
        player_id = str(uuid.uuid4())
        session_token = RoomService.generate_token()

        while db.query(Player).filter(Player.session_token == session_token).first():
            session_token = RoomService.generate_token()

        player = Player(
            id=player_id,
            room_id=room_id,
            name=player_name,
            session_token=session_token,
            is_alive=True,
            is_connected=True,
            is_ready=False,
            is_host=False,
        )

        db.add(player)
        db.commit()
        db.refresh(player)
        return player

    @staticmethod
    def get_player_by_id(db: Session, player_id: str) -> Player | None:
        return db.query(Player).filter(Player.id == player_id).first()

    @staticmethod
    def get_player_by_token(db: Session, session_token: str) -> Player | None:
        return db.query(Player).filter(Player.session_token == session_token).first()

    @staticmethod
    def get_room_players(db: Session, room_id: str) -> list[Player]:
        return db.query(Player).filter(Player.room_id == room_id).order_by(Player.created_at).all()

    @staticmethod
    def update_player_connection(db: Session, player_id: str, is_connected: bool) -> Player | None:
        player = PlayerService.get_player_by_id(db, player_id)
        if player:
            player.is_connected = is_connected
            db.commit()
            db.refresh(player)
        return player

    @staticmethod
    def mark_ready(db: Session, player_id: str, session_token: str, ready: bool = True) -> Player:
        player = PlayerService.get_player_by_id(db, player_id)
        if not player:
            raise ValueError("Player not found")
        if player.session_token != session_token:
            raise PermissionError("Invalid session token")
        player.is_ready = ready
        db.add(player)
        db.commit()
        db.refresh(player)
        return player

    @staticmethod
    def kick_player(db: Session, room_id: str, player_id: str, host_token: str) -> Player:
        room = RoomService.get_room_by_id(db, room_id)
        if not room:
            raise ValueError("Room not found")
        if room.host_token != host_token:
            raise PermissionError("Invalid host token")
        if room.status != RoomStatus.WAITING:
            raise ValueError("Players can only be kicked while the room is waiting")
        player = db.query(Player).filter(Player.id == player_id, Player.room_id == room_id).first()
        if not player:
            raise ValueError("Player not found in this room")
        db.delete(player)
        db.commit()
        return player
