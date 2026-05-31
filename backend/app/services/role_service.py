"""Role service"""
from sqlalchemy.orm import Session
from app.models import Role, DEFAULT_ROLES


class RoleService:
    """Role management service"""
    
    @staticmethod
    def seed_roles(db: Session) -> None:
        """Seed default roles into database if they don't exist"""
        for role_data in DEFAULT_ROLES:
            existing_role = db.query(Role).filter(
                Role.code == role_data["code"]
            ).first()
            
            if not existing_role:
                role = Role(**role_data)
                db.add(role)
        
        db.commit()
    
    @staticmethod
    def get_all_roles(db: Session, active_only: bool = True) -> list[Role]:
        """Get all roles"""
        query = db.query(Role)
        
        if active_only:
            query = query.filter(Role.is_active == True)
        
        return query.order_by(Role.code).all()
    
    @staticmethod
    def get_role_by_code(db: Session, role_code: str) -> Role | None:
        """Get role by code"""
        return db.query(Role).filter(Role.code == role_code).first()
    
    @staticmethod
    def get_roles_by_codes(db: Session, role_codes: list[str]) -> list[Role]:
        """Get multiple roles by codes"""
        return db.query(Role).filter(Role.code.in_(role_codes)).all()
