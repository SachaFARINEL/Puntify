import os
from dotenv import load_dotenv
from motor import motor_asyncio

# load environment variables from .env file
load_dotenv()

# connect to mongodb
client = motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
# select database
db = client.puntify
