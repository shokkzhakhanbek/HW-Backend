from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse

router = APIRouter()


@router.get("/flowers", response_class=HTMLResponse)
def flowers_page(request: Request):
    templates = request.app.state.templates
    flowers = request.app.state.flowers_repo.list_all()
    return templates.TemplateResponse("flowers.html", {
        "request": request,
        "flowers": flowers
    })


@router.post("/flowers")
def add_flower(
    request: Request,
    title: str = Form(...),
    amount: int = Form(...),
    price: float = Form(...)
):
    request.app.state.flowers_repo.create(title=title, amount=amount, price=price)
    return RedirectResponse("/flowers", status_code=303)