from fastapi import FastAPI, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from .routers import users, tracks, auth

templates = Jinja2Templates(directory="app/templates")

app = FastAPI()
app.include_router(
    users.router,
    prefix="/users"
)
app.include_router(
    tracks.router,
    prefix="/tracks"
)
app.include_router(
    auth.router,
    prefix="/auth"
)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("accueil.html", context)


@app.get("/login", response_class=HTMLResponse)
async def root(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("login.html", context)


@app.get("/signIn", response_class=HTMLResponse)
async def root(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("signIn.html", context)
