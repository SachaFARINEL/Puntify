from fastapi import FastAPI, Request, HTTPException as StarletteHTTPException
from fastapi.exception_handlers import http_exception_handler, request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from . import db
from .dependencies import templates
from .ressources.utils import duration_to_time, time_to_minutes
from .routers import users, tracks, auth, admin, home

app = FastAPI()

app.include_router(
    home.router,
    prefix="/home"
)
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
app.include_router(
    admin.router,
    prefix="/admin"
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return await request_validation_exception_handler(request, exc)


@app.exception_handler(404)
async def custom_404_handler(request, __):
    return templates.TemplateResponse("404.html", {"request": request})


@app.get("/", response_class=HTMLResponse)
async def get_landing(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("landing.html", context)


@app.get("/signIn", response_class=HTMLResponse)
async def sign_in(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("user/signUp.html", context)


@app.get("/test", response_class=HTMLResponse)
async def get_dashboard(request: Request):
    users_count = await db["user"].count_documents({})
    tracks_count = await db["tracks"].count_documents({})

    total_listening_minutes = 0
    num_unique_tags = 0
    total_tags = set()
    async for track in db["tracks"].find({}, {'duration': 1, 'tags': 1, '_id': 0}):
        duration_time = duration_to_time(track["duration"])
        total_listening_minutes += time_to_minutes(duration_time)
        if "tags" in track:
            total_tags.update(track["tags"])
        num_unique_tags = len(total_tags)

    context = {"request": request, "users_count": users_count, "tracks_count": tracks_count,
               "total_listening_minutes": total_listening_minutes, "num_unique_tags": num_unique_tags}
    return templates.TemplateResponse("admin/dashboard.html", context)


