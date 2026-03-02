from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from database import users_col, ledger_col

router = APIRouter(prefix="/auth", tags=["auth"])


class RegisterRequest(BaseModel):
    email: str
    password: str
    role: str = "user"


class LoginRequest(BaseModel):
    email: str
    password: str


class GoogleAuthRequest(BaseModel):
    credential: str
    email: str
    name: Optional[str] = ""
    google_id: str
    picture: Optional[str] = ""


def _user_response(user: dict) -> dict:
    return {
        "user_id": str(user["_id"]),
        "email": user["email"],
        "name": user.get("name", ""),
        "picture": user.get("picture", ""),
        "role": user.get("role", "user"),
        "token": f"token-{user['email']}",
    }


@router.post("/register")
def register(req: RegisterRequest):
    if users_col.find_one({"email": req.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    doc = {
        "email": req.email,
        "password": req.password,
        "role": req.role,
        "provider": "email",
        "created_at": datetime.utcnow(),
    }
    result = users_col.insert_one(doc)
    ledger_col.insert_one({
        "user_email": req.email,
        "type": "credit",
        "amount": 0,
        "description": "Welcome to EquiBridge!",
        "timestamp": datetime.utcnow(),
    })
    return {"message": "Registration successful", **_user_response({**doc, "_id": result.inserted_id})}


@router.post("/login")
def login(req: LoginRequest):
    user = users_col.find_one({"email": req.email, "password": req.password})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful", **_user_response(user)}


@router.post("/google")
def google_auth(req: GoogleAuthRequest):
    user = users_col.find_one({"email": req.email})
    if not user:
        doc = {
            "email": req.email,
            "name": req.name,
            "picture": req.picture,
            "google_id": req.google_id,
            "password": f"google_{req.google_id}",
            "role": "user",
            "provider": "google",
            "created_at": datetime.utcnow(),
        }
        result = users_col.insert_one(doc)
        user = {**doc, "_id": result.inserted_id}
        ledger_col.insert_one({
            "user_email": req.email,
            "type": "credit",
            "amount": 0,
            "description": f"Welcome to EquiBridge! (Google: {req.name})",
            "timestamp": datetime.utcnow(),
        })
    return {"message": "Google sign-in successful", **_user_response(user)}
