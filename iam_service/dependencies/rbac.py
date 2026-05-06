from fastapi import Depends, HTTPException
from dependencies.auth import get_current_user


# Role-based access
def require_role(role: str):
    def checker(user=Depends(get_current_user)):
        if role not in user.roles:
            raise HTTPException(status_code=403, detail="Forbidden: role required")
        return user
    return checker


# Permission-based access (recommended)
def require_permission(permission: str):
    def checker(user=Depends(get_current_user)):
        if permission not in user.permissions:
            raise HTTPException(status_code=403, detail="Permission denied")
        return user
    return checker


# Multiple permissions (ANY)
def require_any_permission(permissions: list[str]):
    def checker(user=Depends(get_current_user)):
        if not any(p in user.permissions for p in permissions):
            raise HTTPException(status_code=403, detail="No required permission found")
        return user
    return checker


# Multiple permissions (ALL)
def require_all_permissions(permissions: list[str]):
    def checker(user=Depends(get_current_user)):
        if not all(p in user.permissions for p in permissions):
            raise HTTPException(status_code=403, detail="Missing required permissions")
        return user
    return checker