from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import uuid
from pathlib import Path
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.services.auth_service import register_user
from app.core.security import hash_password
from app.core.dependencies import admin_only, get_current_user

router = APIRouter()

UPLOAD_DIR = Path("uploads/avatars")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


# ───── CURRENT USER ROUTES (must come first) ─────

@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.patch("/me", response_model=UserOut)
def update_me(
    payload: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update current user's own profile (email, full_name)."""
    data = payload.model_dump(exclude_unset=True)
    # Users can't change their own role or active status
    data.pop("role", None)
    data.pop("is_active", None)

    # Check email uniqueness
    if "email" in data and data["email"] != current_user.email:
        existing = db.query(User).filter(User.email == data["email"]).first()
        if existing:
            raise HTTPException(400, "Email already in use")

    for k, v in data.items():
        setattr(current_user, k, v)
    db.commit()
    db.refresh(current_user)
    return current_user


@router.post("/me/avatar", response_model=UserOut)
async def upload_my_avatar(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await _save_avatar(db, current_user, file)


@router.delete("/me/avatar", response_model=UserOut)
def delete_my_avatar(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return _delete_avatar(db, current_user)


# ───── ADMIN ROUTES ─────

@router.get("/", response_model=List[UserOut], dependencies=[Depends(admin_only)])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).order_by(User.id).all()


@router.post("/", response_model=UserOut, dependencies=[Depends(admin_only)])
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    return register_user(db, payload)


# Admin avatar for any user
@router.post("/{user_id}/avatar", response_model=UserOut, dependencies=[Depends(admin_only)])
async def admin_upload_avatar(
    user_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return await _save_avatar(db, user, file)


@router.delete("/{user_id}/avatar", response_model=UserOut, dependencies=[Depends(admin_only)])
def admin_delete_avatar(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return _delete_avatar(db, user)


# Admin reset password for any user
@router.post("/{user_id}/reset-password", response_model=UserOut, dependencies=[Depends(admin_only)])
def admin_reset_password(
    user_id: int,
    payload: dict,
    db: Session = Depends(get_db),
):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(404, "User not found")

    new_password = payload.get("new_password", "")
    if len(new_password) < 6:
        raise HTTPException(400, "Password must be at least 6 characters")

    user.password_hash = hash_password(new_password)
    db.commit()
    db.refresh(user)
    return user


@router.get("/{user_id}", response_model=UserOut, dependencies=[Depends(admin_only)])
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return user


@router.patch("/{user_id}", response_model=UserOut, dependencies=[Depends(admin_only)])
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(404, "User not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(user, k, v)
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", dependencies=[Depends(admin_only)])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(404, "User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted"}


# ───── HELPERS ─────

async def _save_avatar(db: Session, user: User, file: UploadFile) -> User:
    ext = Path(file.filename or "").suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            400,
            f"Invalid file type. Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}",
        )

    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(400, "File too large. Max 5MB.")

    filename = f"user_{user.id}_{uuid.uuid4().hex[:8]}{ext}"
    filepath = UPLOAD_DIR / filename

    with open(filepath, "wb") as f:
        f.write(contents)

    # Delete old
    if user.avatar_url:
        old_name = user.avatar_url.rsplit("/", 1)[-1]
        old_path = UPLOAD_DIR / old_name
        if old_path.exists():
            try:
                old_path.unlink()
            except Exception:
                pass

    user.avatar_url = f"/uploads/avatars/{filename}"
    db.commit()
    db.refresh(user)
    return user


def _delete_avatar(db: Session, user: User) -> User:
    if user.avatar_url:
        old_name = user.avatar_url.rsplit("/", 1)[-1]
        old_path = UPLOAD_DIR / old_name
        if old_path.exists():
            try:
                old_path.unlink()
            except Exception:
                pass
        user.avatar_url = None
        db.commit()
        db.refresh(user)
    return user