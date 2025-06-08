from pymongo import MongoClient
from dotenv import load_dotenv
from fastapi import HTTPException
import os

def iscompatible(location: str, blood_group: str, organ: str):
    load_dotenv(dotenv_path=".env.local")
    MONGODB_URI = os.getenv("MONGODB_URI")

    try:
        client = MongoClient(MONGODB_URI)
        db = client["life_patch"]
        collection = db["donors"]

        query = {
            "address": {"$regex": f"^{location}$", "$options": "i"},
            "blood_group": {"$regex": f"^{blood_group}$", "$options": "i"},
            "organ": {"$regex": f"^{organ}$", "$options": "i"}
        }

        matches = list(collection.find(query))

        for doc in matches:
            doc["_id"] = str(doc["_id"])

        return {"matches": matches}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
