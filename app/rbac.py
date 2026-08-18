from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import User, Role, UserRole
from app.deps import get_current_user

async def get_user_permissions(db: AsyncSession, user_id) -> set[str]:
    result = await db.execute(
        select(Role.permissions).join(UserRole, UserRole.role_id == Role.id).where(UserRole.user_id == user_id)
    )
    perms = set()
    for row in result.scalars().all():
        perms.update(p.strip() for p in row.split(",") if p.strip())
    return perms

def require_permission(permission: str):
    async def checker(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
        perms = await get_user_permissions(db, user.id)
        if permission not in perms and "*" not in perms:
            raise HTTPException(status_code=403, detail={"code": "FORBIDDEN", "message": f"Membutuhkan permission: {permission}"})
        return user
    return checker