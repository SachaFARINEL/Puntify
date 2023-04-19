from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from fastapi import FastAPI
from .routers import users, tracks
templates = Jinja2Templates(directory="app/templates")

app = FastAPI()
app.include_router(users.router)
app.include_router(tracks.router)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("accueil.html", context)
