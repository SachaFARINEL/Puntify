from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from .routers import users, tracks

templates = Jinja2Templates(directory="app/templates")

app = FastAPI()
app.include_router(users.router)
app.include_router(tracks.router)
app.mount("../static", StaticFiles(directory="app/static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("accueil.html", context)
