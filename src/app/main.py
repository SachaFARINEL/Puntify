from fastapi import FastAPI, Request, HTTPException as StarletteHTTPException
from fastapi.exception_handlers import http_exception_handler, request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from .dependencies import templates
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


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("accueil.html", context)


@app.get("/signIn", response_class=HTMLResponse)
async def sign_in(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("signUp.html", context)
