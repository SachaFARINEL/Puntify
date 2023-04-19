import os
from dotenv import load_dotenv
from motor import motor_asyncio

load_dotenv()

client = motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.puntify
