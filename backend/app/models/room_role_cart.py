"""Room Role Cart model"""
from sqlalchemy import Column, String, Integer, ForeignKey, UniqueConstraint
from app.models.base import BaseModel


class RoomRoleCart(BaseModel):
    """Role cart for a room - tracks how many of each role to use"""
    __tablename__ = "room_role_carts"
    
    id = Column(String(36), primary_key=True, index=True)
    room_id = Column(String(36), ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False, index=True)
    role_code = Column(String(50), ForeignKey("roles.code", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, default=0, nullable=False)
    
    # Ensure only one cart entry per room-role combination
    __table_args__ = (
        UniqueConstraint("room_id", "role_code", name="uq_room_role_cart"),
    )
    
    def __repr__(self):
        return f"<RoomRoleCart room={self.room_id} role={self.role_code} qty={self.quantity}>"
