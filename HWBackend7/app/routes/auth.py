import os
import shutil
from fastapi import APIRouter, Request, Form, UploadFile, File, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse

from app.deps import hash_password, verify_password, create_jwt, get_current_user
from app.settings import JWT_COOKIE_NAME, UPLOAD_DIR

router = APIRouter()


@router.get("/signup", response_class=HTMLResponse)
def signup_page(request: Request):
    templates = request.app.state.templates
    return templates.TemplateResponse("signup.html", {"request": request})


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
        return RedirectResponse("/signup", status_code=303)

    photo_filename = None

    if photo and photo.filename:
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        safe_name = os.path.basename(photo.filename)  
        photo_filename = safe_name

        file_path = os.path.join(UPLOAD_DIR, safe_name)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(photo.file, buffer)

    users_repo.create(
        email=email,
        full_name=full_name,
        password_hash=hash_password(password),
        photo_filename=photo_filename
    )

    return RedirectResponse("/login", status_code=303)


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    templates = request.app.state.templates
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    users_repo = request.app.state.users_repo
    user = users_repo.get_by_email(email)

    if not user or not verify_password(password, user.password_hash):
        return RedirectResponse("/login", status_code=303)

    token = create_jwt({"user_id": user.id})

    response = RedirectResponse("/profile", status_code=303)

    response.set_cookie(
        key=JWT_COOKIE_NAME,
        value=token,
        httponly=True,
        samesite="lax",
        path="/",
    )
    return response


@router.get("/profile", response_class=HTMLResponse)
def profile(request: Request):
    templates = request.app.state.templates

    try:
        user = get_current_user(request)
    except HTTPException:
        return RedirectResponse("/login", status_code=303)

    return templates.TemplateResponse("profile.html", {
        "request": request,
        "user": user
    })