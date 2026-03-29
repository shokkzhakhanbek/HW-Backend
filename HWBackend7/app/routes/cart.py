from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from app.settings import CART_COOKIE_NAME

router = APIRouter()


def _get_cart_ids(request: Request) -> list[int]:
    raw = request.cookies.get(CART_COOKIE_NAME)
    if not raw:
        return []
    try:
        return [int(x) for x in raw.split(",") if x.strip() != ""]
    except ValueError:
        return []


def _set_cart_cookie(response, ids: list[int]):
    response.set_cookie(CART_COOKIE_NAME, ",".join(map(str, ids)))


@router.post("/cart/items")
def add_to_cart(request: Request, flower_id: int = Form(...)):
    ids = _get_cart_ids(request)
    ids.append(flower_id)

    response = RedirectResponse("/flowers", status_code=303)
    _set_cart_cookie(response, ids)
    return response


@router.get("/cart/items", response_class=HTMLResponse)
def cart_page(request: Request):
    templates = request.app.state.templates
    flowers_repo = request.app.state.flowers_repo

    ids = _get_cart_ids(request)

    items = []
    total = 0.0

    for fid in ids:
        flower = flowers_repo.get_by_id(fid)
        if flower:
            items.append(flower)
            total += float(flower.price)

    return templates.TemplateResponse("cart.html", {
        "request": request,
        "items": items,
        "total": total
    })