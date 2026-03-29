from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.routes.auth import router as auth_router
from app.routes.flowers import router as flowers_router
from app.routes.cart import router as cart_router
from app.routes.purchased import router as purchased_router
from fastapi.responses import RedirectResponse
from app.repositories.users import UsersRepository
from app.repositories.flowers import FlowersRepository
from app.repositories.purchases import PurchasesRepository

app = FastAPI()

app.state.users_repo = UsersRepository()
app.state.flowers_repo = FlowersRepository()
app.state.purchases_repo = PurchasesRepository()

@app.get("/")
def root():
    return RedirectResponse(url="/flowers")

templates = Jinja2Templates(directory="app/templates")
app.state.templates = templates  

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/app/uploads", StaticFiles(directory="app/uploads"), name="uploads")

app.include_router(auth_router)
app.include_router(flowers_router)
app.include_router(cart_router)
app.include_router(purchased_router)