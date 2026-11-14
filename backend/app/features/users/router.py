from fastapi import APIRouter, Depends

from app.features.users.models import User, UserRead
from app.shared.dependencies import get_current_user

router = APIRouter()


@router.get("/me", response_model=UserRead)
def me(user: User = Depends(get_current_user)) -> User:
    return user
