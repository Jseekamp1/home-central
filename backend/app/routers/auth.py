from fastapi import APIRouter, Header, HTTPException
from supabase_auth.errors import AuthApiError
from pydantic import BaseModel, EmailStr

from app.supabase_client import supabase

router = APIRouter()


class AuthRequest(BaseModel):
    email: EmailStr
    password: str


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
def me(authorization: str = Header(default=None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")

    token = authorization.removeprefix("Bearer ")

    try:
        response = supabase.auth.get_user(token)
    except AuthApiError as e:
        raise HTTPException(status_code=401, detail=str(e))

    return {"id": response.user.id, "email": response.user.email}
