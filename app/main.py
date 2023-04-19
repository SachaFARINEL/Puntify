import os
from motor import motor_asyncio
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from .routers import users, tracks
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.include_router(users.router)
app.include_router(tracks.router)
templates = Jinja2Templates(directory="app/templates")
load_dotenv()

client = motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.college


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("accueil.html", context)
