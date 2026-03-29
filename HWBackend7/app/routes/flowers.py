from fastapi import APIRouter, Request, Form

router = APIRouter()


@router.get("/flowers")
def get_flowers(request: Request):
    flowers = request.app.state.flowers_repo.list_all()

    return [
        {
            "id": f.id,
            "title": f.title,
            "amount": f.amount,
            "price": f.price
        }
        for f in flowers
    ]


@router.post("/flowers")
def add_flower(
    request: Request,
    title: str = Form(...),
    amount: int = Form(...),
    price: float = Form(...)
):
    flower = request.app.state.flowers_repo.create(
        title=title,
        amount=amount,
        price=price
    )

    return {"id": flower.id}