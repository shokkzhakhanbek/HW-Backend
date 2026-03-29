import os
import shutil
from fastapi import APIRouter, Request, Form, UploadFile, File, Depends
from app.deps import hash_password, verify_password, create_jwt, get_current_user
from app.settings import UPLOAD_DIR

router = APIRouter()


@router.post("/signup")
def signup(
    request: Request,
    email: str = Form(...),
    full_name: str = Form(...),
    password: str = Form(...),
    photo: UploadFile = File(None)  
):
    users_repo = request.app.state.users_repo

    if users_repo.get_by_email(email):
        return {"detail": "Email already registered"}

    photo_filename = None
    if photo and photo.filename:
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        safe_name = os.path.basename(photo.filename)
        photo_filename = safe_name
        file_path = os.path.join(UPLOAD_DIR, safe_name)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(photo.file, buffer)

    user = users_repo.create(
        email=email,
        full_name=full_name,
        password_hash=hash_password(password),
        photo_filename=photo_filename
    )

    return {"id": user.id}


@router.post("/login")
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    users_repo = request.app.state.users_repo
    user = users_repo.get_by_email(email)

    if not user or not verify_password(password, user.password_hash):
        return {"detail": "Invalid email or password"}

    token = create_jwt({"user_id": user.id})

    return {"access_token": token, "type": "bearer"}


@router.get("/profile")
def profile(user=Depends(get_current_user)):
    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "photo_filename": user.photo_filename
    }