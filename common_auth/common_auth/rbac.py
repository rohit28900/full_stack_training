from fastapi import Depends, HTTPException


def has_permission(required_permission: str, get_user_dependency):
    """
    RBAC checker
    """

    def checker(user=Depends(get_user_dependency)):

        permissions = user.get("permissions", [])

        if required_permission not in permissions:
            raise HTTPException(
                status_code=403,
                detail=f"Permission '{required_permission}' required"
            )

        return user

    return checker