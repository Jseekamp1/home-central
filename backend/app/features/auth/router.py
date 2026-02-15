from fastapi import APIRouter, Depends, HTTPException
from supabase_auth.errors import AuthApiError

from app.features.auth.models import AuthRequest
from app.shared.dependencies import get_current_user
from app.supabase_client import supabase

router = APIRouter()


@router.post("/signup")
def signup(body: AuthRequest):
    try:
        response = supabase.auth.sign_up(
            {"email": body.email, "password": body.password}
        )
    except AuthApiError as e:
        raise HTTPException(status_code=400, detail=str(e))

    result = {"user": {"id": response.user.id, "email": response.user.email}}

    if response.session:
        result["session"] = {"access_token": response.session.access_token}
    else:
        result["message"] = "Check your email to confirm your account"

    return result


@router.post("/login")
def login(body: AuthRequest):
    try:
        response = supabase.auth.sign_in_with_password(
            {"email": body.email, "password": body.password}
        )
    except AuthApiError as e:
        raise HTTPException(status_code=401, detail=str(e))

    return {
        "user": {"id": response.user.id, "email": response.user.email},
        "session": {"access_token": response.session.access_token},
    }


@router.get("/me")
def me(user: dict = Depends(get_current_user)):
    return user
