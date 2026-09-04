import os
from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from sqlalchemy.orm import Session

from database import SessionLocal
from models import User

router = APIRouter()

oauth = OAuth()
oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/auth/login")
async def login(request: Request):
    redirect_uri = "http://localhost:8000/auth/callback"
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/auth/callback")
async def callback(request: Request, db: Session = Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)
    userinfo = token.get("userinfo")

    # Check if this user already exists (by Google's unique ID)
    user = db.query(User).filter(User.google_sub == userinfo["sub"]).first()

    if not user:
        # First time logging in — create a new row
        user = User(
            google_sub=userinfo["sub"],
            email=userinfo["email"],
            name=userinfo.get("name"),
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    # Remember this user for future requests via the session cookie
    request.session["user_id"] = str(user.id)

    return {"logged_in_as": user.email, "user_id": str(user.id), "new_user": user.name is not None}

@router.get("/auth/me")
async def me(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        return {"authenticated": False}
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"authenticated": False}
    return {"authenticated": True, "email": user.email, "name": user.name}