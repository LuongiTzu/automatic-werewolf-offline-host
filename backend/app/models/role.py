"""Role model"""
from sqlalchemy import Column, String, Integer, Enum as SQLEnum, Boolean
from app.models.base import BaseModel
import enum


class Side(str, enum.Enum):
    """Player faction/side"""
    VILLAGER = "villager"  # Dân Làng
    WEREWOLF = "werewolf"  # Ma Sói
    SPECIAL = "special"    # Phe thứ ba (Cupid, Kẻ tẩm dầu, Thằng Khờ)


class Role(BaseModel):
    """Role/Character model for Werewolf game"""
    __tablename__ = "roles"
    
    code = Column(String(50), primary_key=True, index=True)  # e.g., "VILLAGER", "WEREWOLF"
    name = Column(String(100), nullable=False)  # e.g., "Dân Làng", "Ma Sói"
    side = Column(SQLEnum(Side), nullable=False)  # villager, werewolf, special
    description = Column(String(500), nullable=True)  # Brief description
    night_order = Column(Integer, nullable=True)  # Order to call at night (1, 2, 3, ...)
    is_active = Column(Boolean, default=True, nullable=False)  # Can be used in games
    
    def __repr__(self):
        return f"<Role {self.code}>"


# Default roles data
DEFAULT_ROLES = [
    {
        "code": "VILLAGER",
        "name": "Dân Làng",
        "side": "villager",
        "description": "Không có kỹ năng. Thắng khi toàn bộ Sói chết.",
        "night_order": None,
        "is_active": True,
    },
    {
        "code": "GUARD",
        "name": "Bảo Vệ",
        "side": "villager",
        "description": "Mỗi đêm chọn 1 người để bảo vệ. Không được bảo vệ cùng người trong 2 đêm liên tiếp.",
        "night_order": 2,
        "is_active": True,
    },
    {
        "code": "HUNTER",
        "name": "Thợ Săn",
        "side": "villager",
        "description": "Chọn 1 người để kéo theo nếu bản thân bị chết.",
        "night_order": 3,
        "is_active": True,
    },
    {
        "code": "SEER",
        "name": "Tiên Tri",
        "side": "villager",
        "description": "Mỗi đêm chọn 1 người để soi (Sói hay không).",
        "night_order": 7,
        "is_active": True,
    },
    {
        "code": "WITCH",
        "name": "Phù Thủy",
        "side": "villager",
        "description": "Có 2 bình: cứu và độc. Mỗi bình dùng 1 lần trong cả game.",
        "night_order": 6,
        "is_active": True,
    },
    {
        "code": "WEREWOLF",
        "name": "Ma Sói",
        "side": "werewolf",
        "description": "Thấy nhau, vote chọn người để cắn. Thắng khi số Sói >= số Dân.",
        "night_order": 5,
        "is_active": True,
    },
    {
        "code": "CURSED_WOLF",
        "name": "Sói Nguyền",
        "side": "villager",  # Starts as villager
        "description": "Ban đầu là Dân. Nếu bị Sói cắn thì hóa thành Sói.",
        "night_order": None,
        "is_active": True,
    },
    {
        "code": "CUPID",
        "name": "Cupid",
        "side": "special",
        "description": "Đêm đầu ghép đôi 2 người. Nếu một người chết, người kia cũng chết.",
        "night_order": 1,
        "is_active": True,
    },
    {
        "code": "OILMAN",
        "name": "Kẻ Tẩm Dầu",
        "side": "special",
        "description": "Mỗi đêm chọn tối đa 2 người. Thắng khi tất cả còn sống đều bị tẩm dầu.",
        "night_order": 1,
        "is_active": True,
    },
    {
        "code": "FOOL",
        "name": "Thằng Khờ",
        "side": "special",
        "description": "Nếu bị treo cổ, game kết thúc ngay. Thằng Khờ thắng.",
        "night_order": None,
        "is_active": True,
    },
]
