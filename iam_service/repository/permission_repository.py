from sqlmodel import Session, select
from models.permission import Permission
from models.mapping import UserRole, RolePermission


class PermissionRepository:

    # Create
    def create(self, db: Session, permission: Permission):
        try:
            db.add(permission)
            db.commit()
            db.refresh(permission)
            return permission
        except Exception as e:
            db.rollback()
            raise e

    # Get by name
    def get_by_name(self, db: Session, name: str):
        statement = select(Permission).where(Permission.name == name)
        return db.exec(statement).first()

    # Get all
    def get_all(self, db: Session):
        statement = select(Permission)
        return db.exec(statement).all()
    

    #Get permissions by user_id (FIXED - REQUIRED)
    def get_permissions_by_user_id(self, db: Session, user_id):
        statement = (
            select(Permission)
            .join(RolePermission, Permission.id == RolePermission.permission_id)
            .join(UserRole, RolePermission.role_id == UserRole.role_id)
            .where(UserRole.user_id == user_id)
        )
        return db.exec(statement).all()

    # Check if role already has permission
    def get_role_permission(self, db: Session, role_id, permission_id):
        statement = select(RolePermission).where(
            RolePermission.role_id == role_id,
            RolePermission.permission_id == permission_id
        )
        return db.exec(statement).first()