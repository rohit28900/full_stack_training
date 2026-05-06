from sqlmodel import Session, select
from models.role import Role
from models.mapping import RolePermission, UserRole


class RoleRepository:

    # ✅ Create
    def create(self, db: Session, role: Role):
        try:
            db.add(role)
            db.commit()
            db.refresh(role)
            return role
        except Exception as e:
            db.rollback()
            raise e

    # ✅ Get by name
    def get_by_name(self, db: Session, name: str):
        statement = select(Role).where(Role.name == name)
        return db.exec(statement).first()

    # ✅ Get all
    def get_all(self, db: Session):
        statement = select(Role)
        return db.exec(statement).all()

    # ✅ Get roles by user_id (FIXED - REQUIRED FOR LOGIN)
    def get_roles_by_user_id(self, db: Session, user_id):
        statement = (
            select(Role)
            .join(UserRole, Role.id == UserRole.role_id)
            .where(UserRole.user_id == user_id)
        )
        return db.exec(statement).all()

    # ✅ Assign permission to role
    def assign_permission(self, db: Session, role_id, permission_id):
        try:
            mapping = RolePermission(
                role_id=role_id,
                permission_id=permission_id
            )
            db.add(mapping)
            db.commit()
            return mapping
        except Exception as e:
            db.rollback()
            raise e

    # ✅ Check if permission already assigned
    def get_role_permission(self, db: Session, role_id, permission_id):
        statement = select(RolePermission).where(
            RolePermission.role_id == role_id,
            RolePermission.permission_id == permission_id
        )
        return db.exec(statement).first()

    # ✅ Assign role to user (NEW - you’ll need this next)
    def assign_role_to_user(self, db: Session, user_id, role_id):
        try:
            mapping = UserRole(
                user_id=user_id,
                role_id=role_id
            )
            db.add(mapping)
            db.commit()
            return mapping
        except Exception as e:
            db.rollback()
            raise e

    # ✅ Check if user already has role
    def get_user_role(self, db: Session, user_id, role_id):
        statement = select(UserRole).where(
            UserRole.user_id == user_id,
            UserRole.role_id == role_id
        )
        return db.exec(statement).first()