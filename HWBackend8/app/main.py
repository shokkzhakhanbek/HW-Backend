from fastapi import FastAPI, Depends, HTTPException, Cookie
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from database import get_db
from repositories import UsersRepository, FlowersRepository, PurchasesRepository
from auth import create_access_token, get_current_user_id

app = FastAPI()

users_repo = UsersRepository()
flowers_repo = FlowersRepository()
purchases_repo = PurchasesRepository()


class UserCreate(BaseModel):
    email: str
    full_name: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class FlowerCreate(BaseModel):
    name: str
    count: int
    cost: float

class FlowerUpdate(BaseModel):
    name: Optional[str] = None
    count: Optional[int] = None
    cost: Optional[float] = None



@app.post("/signup")
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    
    existing_user = users_repo.get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Existing user with this email")

    new_user = users_repo.create_user(
        db=db,
        email=user_data.email,
        full_name=user_data.full_name,
        password=user_data.password 
    )

    return {"id": new_user.id, "email": new_user.email}


@app.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    
    user = users_repo.get_user_by_email(db, user_data.email)

    if user is None or user.password != user_data.password:
        raise HTTPException(status_code=401, detail="Not correct email or password")

    token = create_access_token(data={"user_id": user.id})

    return {"access_token": token, "token_type": "bearer"}


@app.get("/profile")
def get_profile(
    user_id: int = Depends(get_current_user_id),  
    db: Session = Depends(get_db)
):
    
    user = users_repo.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name
    }


@app.get("/flowers")
def get_flowers(db: Session = Depends(get_db)):
    flowers = flowers_repo.get_all_flowers(db)

    return [
        {
            "id": f.id,
            "name": f.name,
            "count": f.count,
            "cost": f.cost
        }
        for f in flowers
    ]


@app.post("/flowers")
def create_flower(
    flower_data: FlowerCreate,
    db: Session = Depends(get_db)
):
    new_flower = flowers_repo.create_flower(
        db=db,
        name=flower_data.name,
        count=flower_data.count,
        cost=flower_data.cost
    )
    return {"id": new_flower.id, "name": new_flower.name}


@app.patch("/flowers/{flower_id}")
def update_flower(
    flower_id: int,
    flower_data: FlowerUpdate,
    db: Session = Depends(get_db)
):
    updated = flowers_repo.update_flower(
        db=db,
        flower_id=flower_id,
        name=flower_data.name,
        count=flower_data.count,
        cost=flower_data.cost
    )

    if updated is None:
        raise HTTPException(status_code=404, detail="Flower not found")

    return {
        "id": updated.id,
        "name": updated.name,
        "count": updated.count,
        "cost": updated.cost
    }


@app.delete("/flowers/{flower_id}")
def delete_flower(flower_id: int, db: Session = Depends(get_db)):
    deleted = flowers_repo.delete_flower(db, flower_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Flower not found")

    return {"detail": "Цветок удалён"}


@app.post("/cart/items")
def add_to_cart(
    flower_id: int,
    cart: str = Cookie(default=""),  
    db: Session = Depends(get_db)
):
    flower = flowers_repo.get_flower_by_id(db, flower_id)
    if flower is None:
        raise HTTPException(status_code=404, detail="Flowers not found")

    cart_items = cart.split(",") if cart else []
    cart_items.append(str(flower_id))
    new_cart = ",".join(cart_items)

    response = JSONResponse(content={"detail": "Added to cart"})
    response.set_cookie(key="cart", value=new_cart)
    return response


@app.get("/cart/items")
def get_cart_items(
    cart: str = Cookie(default=""),
    db: Session = Depends(get_db)
):
    if not cart:
        return []

    flower_ids = [int(x) for x in cart.split(",") if x]

    result = []
    for fid in flower_ids:
        flower = flowers_repo.get_flower_by_id(db, fid)
        if flower:
            result.append({
                "id": flower.id,
                "name": flower.name,
                "cost": flower.cost
            })

    return result


@app.post("/purchased")
def purchase_items(
    user_id: int = Depends(get_current_user_id),
    cart: str = Cookie(default=""),
    db: Session = Depends(get_db)
):
    
    if not cart:
        raise HTTPException(status_code=400, detail="Chart is empty")

    flower_ids = [int(x) for x in cart.split(",") if x]

    for fid in flower_ids:
        purchases_repo.create_purchase(db=db, user_id=user_id, flower_id=fid)

    response = JSONResponse(content={"detail": "Purchase successful"})
    response.delete_cookie(key="cart")
    return response


@app.get("/purchased")
def get_purchased(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    purchases = purchases_repo.get_purchases_by_user(db, user_id)

    return [
        {
            "id": p.id,
            "user_id": p.user_id,
            "flower": {
                "id": p.flower.id,
                "name": p.flower.name,
                "cost": p.flower.cost
            }
        }
        for p in purchases
    ]