from repository.role_repository import RoleRepository
from repository.permission_repository import PermissionRepository
from models.role import Role


class RoleService:

    def __init__(self):
        self.repo = RoleRepository()
        self.permission_repo = PermissionRepository()

    # Create Role
    def create_role(self, db, data):
        try:
            existing = self.repo.get_by_name(db, data.name)
            if existing:
                raise ValueError("Role already exists")

            role = Role(name=data.name)

            return self.repo.create(db, role)

        except ValueError:
            raise

        except Exception as e:
            raise RuntimeError(f"Error creating role: {str(e)}")

    #Get All Roles
    def get_all_roles(self, db):
        try:
            return self.repo.get_all(db)

        except Exception as e:
            raise RuntimeError(f"Error fetching roles: {str(e)}")

    # Assign Permission to Role
    def assign_permission_to_role(self, db, role_id, permission_id):
        try:
            existing = self.repo.get_role_permission(db, role_id, permission_id)

            if existing:
                raise ValueError("Permission already assigned to role")

            return self.repo.assign_permission(db, role_id, permission_id)

        except ValueError:
            raise

        except Exception as e:
            raise RuntimeError(f"Error assigning permission: {str(e)}")