from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
import hashlib

from core.config import settings
from repository.user_repository import UserRepository
from repository.role_repository import RoleRepository
from repository.permission_repository import PermissionRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:

    def __init__(self):
        self.user_repo = UserRepository()
        self.role_repo = RoleRepository()
        self.permission_repo = PermissionRepository()

    # Password verification (FIXED)
    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        pre_hashed = hashlib.sha256(plain_password.encode()).hexdigest()
        print(f"Pre-hashed password: {pre_hashed}")  # Debugging line
        return pwd_context.verify(pre_hashed, hashed_password)

    #Authenticate User
    def authenticate(self, db, email, password):
        try:
            user = self.user_repo.get_by_email(db, email)

            if not user:
                return None

            if not self._verify_password(password, user.password_hash):
                return None

            return user

        except Exception as e:
            raise RuntimeError(f"Authentication failed: {str(e)}")

    # Build JWT payload
    def build_payload(self, db, user):
        try:
            roles = self.role_repo.get_roles_by_user_id(db, user.id) or []
            permissions = self.permission_repo.get_permissions_by_user_id(db, user.id) or []

            print("ROLES:", roles)
            print("PERMISSIONS:", permissions)

            return {
                "sub": str(user.id),
                "roles": [r.name for r in roles],
                "permissions": [p.name for p in permissions]
            }

        except Exception as e:
            print("ERROR IN PAYLOAD:", str(e))
            raise RuntimeError(f"Failed to build token payload: {str(e)}")

    # Create JWT token
    def create_token(self, payload: dict):
        try:
            payload_copy = payload.copy()  # avoid mutating original

            payload_copy["exp"] = datetime.utcnow() + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )

            return jwt.encode(
                payload_copy,
                settings.SECRET_KEY,
                algorithm=settings.ALGORITHM
            )

        except Exception as e:
            raise RuntimeError(f"Token creation failed: {str(e)}")