"""Player service"""
import uuid
from sqlalchemy.orm import Session
from app.models import Player
from app.services.room_service import RoomService


class PlayerService:
    """Player business logic service"""
    
    @staticmethod
    def join_room(db: Session, room_id: str, player_name: str) -> Player:
        """Create a new player and join a room"""
        player_id = str(uuid.uuid4())
        session_token = RoomService.generate_token()
        
        # Ensure session_token is unique
        while db.query(Player).filter(Player.session_token == session_token).first():
            session_token = RoomService.generate_token()
        
        player = Player(
            id=player_id,
            room_id=room_id,
            name=player_name,
            session_token=session_token,
            is_alive=True,
            is_connected=True,
        )
        
        db.add(player)
        db.commit()
        db.refresh(player)
        
        return player
    
    @staticmethod
    def get_player_by_id(db: Session, player_id: str) -> Player | None:
        """Get player by ID"""
        return db.query(Player).filter(Player.id == player_id).first()
    
    @staticmethod
    def get_player_by_token(db: Session, session_token: str) -> Player | None:
        """Get player by session token"""
        return db.query(Player).filter(Player.session_token == session_token).first()
    
    @staticmethod
    def get_room_players(db: Session, room_id: str) -> list[Player]:
        """Get all players in a room"""
        return db.query(Player).filter(Player.room_id == room_id).order_by(Player.joined_at).all()
    
    @staticmethod
    def update_player_connection(db: Session, player_id: str, is_connected: bool) -> Player | None:
        """Update player connection status"""
        player = PlayerService.get_player_by_id(db, player_id)
        if player:
            player.is_connected = is_connected
            db.commit()
            db.refresh(player)
        return player
