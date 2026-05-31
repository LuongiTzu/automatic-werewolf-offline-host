"""Role Cart service"""
import uuid
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import RoomRoleCart, Role, Player
from app.services.room_service import RoomService


class RoleCartService:
    """Role cart management service"""
    
    @staticmethod
    def initialize_cart_for_room(db: Session, room_id: str) -> None:
        """Initialize empty role cart for a new room"""
        from app.models import DEFAULT_ROLES
        
        # Create cart entry for each role with quantity 0
        for role_data in DEFAULT_ROLES:
            existing = db.query(RoomRoleCart).filter(
                RoomRoleCart.room_id == room_id,
                RoomRoleCart.role_code == role_data["code"]
            ).first()
            
            if not existing:
                cart_item = RoomRoleCart(
                    id=str(uuid.uuid4()),
                    room_id=room_id,
                    role_code=role_data["code"],
                    quantity=0,
                )
                db.add(cart_item)
        
        db.commit()
    
    @staticmethod
    def get_room_cart(db: Session, room_id: str) -> list[RoomRoleCart]:
        """Get all cart items for a room"""
        return db.query(RoomRoleCart).filter(
            RoomRoleCart.room_id == room_id
        ).all()
    
    @staticmethod
    def get_cart_with_details(db: Session, room_id: str) -> list[dict]:
        """Get cart items with role details (name, code, quantity)"""
        cart_items = RoleCartService.get_room_cart(db, room_id)
        
        result = []
        for item in cart_items:
            role = db.query(Role).filter(Role.code == item.role_code).first()
            if role:
                result.append({
                    "role_code": item.role_code,
                    "name": role.name,
                    "quantity": item.quantity,
                })
        
        return result
    
    @staticmethod
    def update_cart(
        db: Session,
        room_id: str,
        roles_update: list[dict]
    ) -> list[RoomRoleCart]:
        """
        Update role cart for a room.
        
        Args:
            db: Database session
            room_id: Room ID
            roles_update: List of dicts with 'role_code' and 'quantity'
        
        Returns:
            Updated cart items
        """
        # Validate all role codes exist
        role_codes = [r["role_code"] for r in roles_update]
        existing_roles = db.query(Role).filter(Role.code.in_(role_codes)).all()
        existing_role_codes = {r.code for r in existing_roles}
        
        for role_code in role_codes:
            if role_code not in existing_role_codes:
                raise ValueError(f"Role '{role_code}' does not exist")
        
        # Validate quantities are non-negative
        for role_update in roles_update:
            if role_update["quantity"] < 0:
                raise ValueError(
                    f"Quantity for role '{role_update['role_code']}' cannot be negative"
                )
        
        # Update quantities
        updated_items = []
        for role_update in roles_update:
            cart_item = db.query(RoomRoleCart).filter(
                RoomRoleCart.room_id == room_id,
                RoomRoleCart.role_code == role_update["role_code"]
            ).first()
            
            if cart_item:
                cart_item.quantity = role_update["quantity"]
                db.add(cart_item)
                updated_items.append(cart_item)
        
        db.commit()
        
        # Refresh all items
        for item in updated_items:
            db.refresh(item)
        
        return updated_items
    
    @staticmethod
    def get_total_roles(db: Session, room_id: str) -> int:
        """Get total number of roles in cart for a room"""
        result = db.query(func.sum(RoomRoleCart.quantity)).filter(
            RoomRoleCart.room_id == room_id
        ).scalar()
        
        return result or 0
    
    @staticmethod
    def get_cart_summary(
        db: Session,
        room_id: str
    ) -> dict:
        """
        Get cart summary for a room.
        
        Returns:
            {
                'total_roles': int,
                'total_players': int,
                'can_start': bool,
                'cart_items': list,
            }
        """
        total_roles = RoleCartService.get_total_roles(db, room_id)
        total_players = RoomService.get_player_count(db, room_id)
        cart_items = RoleCartService.get_cart_with_details(db, room_id)
        
        return {
            "total_roles": total_roles,
            "total_players": total_players,
            "can_start": total_roles >= total_players,
            "cart_items": cart_items,
        }
