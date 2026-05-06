from repository.permission_repository import PermissionRepository
from models.permission import Permission


class PermissionService:

    def __init__(self):
        self.repo = PermissionRepository()

    # Create Permission
    def create_permission(self, db, data):
        try:
            existing = self.repo.get_by_name(db, data.name)
            if existing:
                raise ValueError("Permission already exists")

            permission = Permission(name=data.name)

            return self.repo.create(db, permission)

        except ValueError:
            raise

        except Exception as e:
            raise RuntimeError(f"Error creating permission: {str(e)}")

    # Get All Permissions
    def get_all_permissions(self, db):
        try:
            return self.repo.get_all(db)

        except Exception as e:
            raise RuntimeError(f"Error fetching permissions: {str(e)}")