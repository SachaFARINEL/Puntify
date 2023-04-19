import os
from motor import motor_asyncio
from dotenv import load_dotenv
from fastapi import FastAPI
from routers import users, tracks

app = FastAPI()
app.include_router(users.router)
app.include_router(tracks.router)
load_dotenv()


client = motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.college



@app.get("/")
async def root():
    return {"message": "Hello World"}

