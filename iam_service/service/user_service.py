from repository.user_repository import UserRepository
from repository.role_repository import RoleRepository
from models.user import User
from passlib.context import CryptContext
import hashlib

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:

    def __init__(self):
        self.repo = UserRepository()
        self.role_repo = RoleRepository()

    # Create User
    def create_user(self, db, data):
        try:
            existing = self.repo.get_by_email(db, data.email)
            if existing:
                raise ValueError("User already exists")

            # hashed = pwd_context.hash(data.password)
            pre_hashed = hashlib.sha256(data.password.encode()).hexdigest()
            hashed = pwd_context.hash(pre_hashed)

            user = User(
                email=data.email,
                password_hash=hashed
            )

            return self.repo.create(db, user)

        except ValueError:
            raise

        except Exception as e:
            raise RuntimeError(f"Error creating user: {str(e)}")

    # Get User by ID
    def get_user_by_id(self, db, user_id):
        try:
            return self.repo.get_by_id(db, user_id)

        except Exception as e:
            raise RuntimeError(f"Error fetching user: {str(e)}")

    # Get All Users
    def get_all_users(self, db):
        try:
            return self.repo.get_all(db)

        except Exception as e:
            raise RuntimeError(f"Error fetching users: {str(e)}")

    # Update User
    def update_user(self, db, user_id, data):
        try:
            user = self.repo.get_by_id(db, user_id)
            if not user:
                return None

            # update fields only if provided
            if data.email:
                # check duplicate email
                existing = self.repo.get_by_email(db, data.email)
                if existing and existing.id != user_id:
                    raise ValueError("Email already in use")
                user.email = data.email

            if data.is_active is not None:
                user.is_active = data.is_active

            return self.repo.update(db, user)

        except ValueError:
            raise

        except Exception as e:
            raise RuntimeError(f"Error updating user: {str(e)}")

    # Delete User
    def delete_user(self, db, user_id):
        try:
            return self.repo.delete(db, user_id)

        except Exception as e:
            raise RuntimeError(f"Error deleting user: {str(e)}")
        
    
    def assign_role_to_user(self, db, user_id, role_id):
        try:
            user = self.repo.get_by_id(db, user_id)
            if not user:
                raise ValueError("User not found")

            # role = self.role_repo.get_by_id(db, role_id)
            # if not role:
            #     raise ValueError("Role not found")

            existing = self.role_repo.get_user_role(db, user_id, role_id)
            if existing:
                raise ValueError("Role already assigned to user")

            return self.role_repo.assign_role_to_user(db, user_id, role_id)

        except ValueError:
            raise

        except Exception as e:
            raise RuntimeError(f"Error assigning role: {str(e)}")