from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from app.settings import CART_COOKIE_NAME
from app.deps import get_current_user

router = APIRouter()


def _get_cart_ids(request: Request) -> list[int]:
    raw = request.cookies.get(CART_COOKIE_NAME)
    if not raw:
        return []
    try:
        return [int(x) for x in raw.split(",") if x.strip() != ""]
    except ValueError:
        return []

@router.post("/purchased")
def make_purchase(request: Request, user=Depends(get_current_user)):
    cart_ids = _get_cart_ids(request)
    purchases_repo = request.app.state.purchases_repo

    for flower_id in cart_ids:
        purchases_repo.add(user_id=user.id, flower_id=flower_id)

    response = JSONResponse(content={"detail": "OK"})
    response.delete_cookie(CART_COOKIE_NAME)
    return response


@router.get("/purchased")
def purchased_list(request: Request, user=Depends(get_current_user)):
    purchases_repo = request.app.state.purchases_repo
    flowers_repo = request.app.state.flowers_repo

    purchases = purchases_repo.list_by_user(user.id)

    items = []
    total = 0.0

    for p in purchases:
        flower = flowers_repo.get_by_id(p.flower_id)
        if flower:
            items.append({
                "title": flower.title,
                "price": flower.price
            })
            total += float(flower.price)

    return {
        "items": items,
        "total": total
    }