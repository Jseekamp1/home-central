from fastapi import Depends, Header, HTTPException
from supabase import Client, ClientOptions, create_client
from supabase_auth.errors import AuthApiError

from app.config import settings
from app.supabase_client import supabase


def get_current_user(authorization: str = Header(default=None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")

    token = authorization.removeprefix("Bearer ")

    try:
        response = supabase.auth.get_user(token)
    except AuthApiError as e:
        raise HTTPException(status_code=401, detail=str(e))

    return {"id": response.user.id, "email": response.user.email, "token": token}


def get_authenticated_client(user: dict = Depends(get_current_user)) -> Client:
    return create_client(
        settings.supabase_url,
        settings.supabase_key,
        options=ClientOptions(headers={"Authorization": f"Bearer {user['token']}"}),
    )
