from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
import random
import string
from app.database import get_db
from app.schemas.token import TokenWithUser
from app.schemas.user import UserOut
from app.services.auth_service import authenticate, make_token
from app.services.email_service import send_reset_code
from app.core.dependencies import get_current_user
from app.core.security import hash_password
from app.models.user import User

router = APIRouter()

# In-memory reset codes. Production mein Redis ya DB use karo.
RESET_CODES = {}


@router.post("/login", response_model=TokenWithUser)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = authenticate(db, form_data.username, form_data.password)
    token = make_token(user)
    return {"access_token": token, "token_type": "bearer", "user": user}


@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return current_user


# ───── FORGOT PASSWORD ─────

@router.post("/forgot-password")
def forgot_password(payload: dict, db: Session = Depends(get_db)):
    """
    Generate reset code and send via email.
    If email not configured, code is printed to console AND returned (dev mode).
    """
    email = (payload.get("email") or "").strip().lower()
    if not email:
        raise HTTPException(400, "Email required")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        # Don't reveal if user exists (security)
        return {"message": "If email exists, code sent"}

    # Generate 6-digit code
    code = "".join(random.choices(string.digits, k=6))
    RESET_CODES[email] = {
        "code": code,
        "expires": datetime.now(timezone.utc) + timedelta(minutes=15),
        "user_id": user.id,
    }

    # Try to send email
    sent = send_reset_code(email, code)

    if sent:
        return {"message": "Reset code sent to your email"}
    else:
        # Dev mode: SMTP not configured — return code for testing
        return {
            "message": "Dev mode: SMTP not configured, code shown here",
            "dev_code": code,
        }


@router.post("/verify-reset-code")
def verify_reset_code(payload: dict):
    """Verify the reset code."""
    email = (payload.get("email") or "").strip().lower()
    code = (payload.get("code") or "").strip()

    entry = RESET_CODES.get(email)
    if not entry:
        raise HTTPException(400, "Invalid or expired code")

    if datetime.now(timezone.utc) > entry["expires"]:
        del RESET_CODES[email]
        raise HTTPException(400, "Code expired")

    if entry["code"] != code:
        raise HTTPException(400, "Invalid code")

    return {"message": "Code verified", "valid": True}


@router.post("/reset-password")
def reset_password(payload: dict, db: Session = Depends(get_db)):
    """Reset password using verified code."""
    email = (payload.get("email") or "").strip().lower()
    code = (payload.get("code") or "").strip()
    new_password = payload.get("new_password") or ""

    if len(new_password) < 6:
        raise HTTPException(400, "Password must be at least 6 characters")

    entry = RESET_CODES.get(email)
    if not entry or entry["code"] != code:
        raise HTTPException(400, "Invalid code")

    if datetime.now(timezone.utc) > entry["expires"]:
        del RESET_CODES[email]
        raise HTTPException(400, "Code expired")

    user = db.query(User).get(entry["user_id"])
    if not user:
        raise HTTPException(404, "User not found")

    user.password_hash = hash_password(new_password)
    db.commit()

    del RESET_CODES[email]

    return {"message": "Password reset successful"}