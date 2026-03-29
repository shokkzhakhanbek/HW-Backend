from fastapi import FastAPI

from app.routes.auth import router as auth_router
from app.routes.flowers import router as flowers_router
from app.routes.cart import router as cart_router
from app.routes.purchased import router as purchased_router
from app.repositories.users import UsersRepository
from app.repositories.flowers import FlowersRepository
from app.repositories.purchases import PurchasesRepository

app = FastAPI()

app.state.users_repo = UsersRepository()
app.state.flowers_repo = FlowersRepository()
app.state.purchases_repo = PurchasesRepository()

app.include_router(auth_router)
app.include_router(flowers_router)
app.include_router(cart_router)
app.include_router(purchased_router)