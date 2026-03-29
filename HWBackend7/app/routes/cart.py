from fastapi import APIRouter, Request, Form
from fastapi.responses import JSONResponse
from app.settings import CART_COOKIE_NAME

router = APIRouter()


def _get_cart_ids(request: Request) -> list[int]:
    """Достаём список id цветов из куки."""
    raw = request.cookies.get(CART_COOKIE_NAME)
    if not raw:
        return []
    try:
        return [int(x) for x in raw.split(",") if x.strip() != ""]
    except ValueError:
        return []


@router.post("/cart/items")
def add_to_cart(request: Request, flower_id: int = Form(...)):
    ids = _get_cart_ids(request)
    ids.append(flower_id)

    response = JSONResponse(content={"detail": "OK"})
    response.set_cookie(CART_COOKIE_NAME, ",".join(map(str, ids)))
    return response


@router.get("/cart/items")
def cart_items(request: Request):
    flowers_repo = request.app.state.flowers_repo
    ids = _get_cart_ids(request)

    items = []
    total = 0.0

    for fid in ids:
        flower = flowers_repo.get_by_id(fid)
        if flower:
            items.append({
                "id": flower.id,
                "title": flower.title,
                "price": flower.price
            })
            total += float(flower.price)

    return {
        "items": items,
        "total": total
    }