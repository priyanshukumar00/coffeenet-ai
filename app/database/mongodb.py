import os
import certifi

from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")

client = MongoClient(
    MONGODB_URL,
    tlsCAFile=certifi.where()
)

database = client["coffeenet_ai"]