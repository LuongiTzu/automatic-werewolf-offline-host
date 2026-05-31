"""Room service"""
import uuid
import secrets
import string
from sqlalchemy.orm import Session
from app.models import Room, Player, RoomStatus, GamePhase


class RoomService:
    """Room business logic service"""
    
    @staticmethod
    def generate_room_code(length: int = 6) -> str:
        """Generate a random room code (e.g., 'ABC123')"""
        characters = string.ascii_uppercase + string.digits
        return ''.join(secrets.choice(characters) for _ in range(length))
    
    @staticmethod
    def generate_token(length: int = 64) -> str:
        """Generate a secure random token"""
        return secrets.token_hex(length // 2)
    
    @staticmethod
    def create_room(db: Session) -> Room:
        """Create a new room"""
        from app.services.role_cart_service import RoleCartService
        
        room_id = str(uuid.uuid4())
        room_code = RoomService.generate_room_code()
        host_token = RoomService.generate_token()
        
        # Ensure room_code is unique
        while db.query(Room).filter(Room.room_code == room_code).first():
            room_code = RoomService.generate_room_code()
        
        room = Room(
            id=room_id,
            room_code=room_code,
            host_token=host_token,
            status=RoomStatus.WAITING,
            current_phase=GamePhase.SETUP,
        )
        
        db.add(room)
        db.commit()
        db.refresh(room)
        
        # Initialize role cart for the room
        RoleCartService.initialize_cart_for_room(db, room_id)
        
        return room
    
    @staticmethod
    def get_room_by_code(db: Session, room_code: str) -> Room | None:
        """Get room by room code"""
        return db.query(Room).filter(Room.room_code == room_code).first()
    
    @staticmethod
    def get_room_by_id(db: Session, room_id: str) -> Room | None:
        """Get room by room ID"""
        return db.query(Room).filter(Room.id == room_id).first()
    
    @staticmethod
    def get_room_players(db: Session, room_id: str) -> list[Player]:
        """Get all players in a room"""
        return db.query(Player).filter(Player.room_id == room_id).all()
    
    @staticmethod
    def get_player_count(db: Session, room_id: str) -> int:
        """Get player count in a room"""
        return db.query(Player).filter(Player.room_id == room_id).count()
    
    @staticmethod
    def verify_host_token(db: Session, room_id: str, host_token: str) -> bool:
        """Verify host token for a room"""
        room = RoomService.get_room_by_id(db, room_id)
        return room is not None and room.host_token == host_token
