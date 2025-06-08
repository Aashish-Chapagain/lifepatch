from pymongo import MongoClient
from fastapi import HTTPException
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env.local")
MONGODB_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGODB_URI)
db = client["life_patch"]
collection = db["donors"]

def iscompatible(location: str, blood_group: str, organ: str):
    try:
        try:
            lat_str, lon_str = location.split(",")
            lat = float(lat_str.strip())
            lon = float(lon_str.strip())
        except Exception:
            raise HTTPException(status_code=400, detail="Location must be in 'lat,lon' format")

        
        query_within_50km = {
            "blood_group": blood_group.upper(),
            "organ": organ.lower(),
            "location": {
                "$near": {
                    "$geometry": {"type": "Point", "coordinates": [lon, lat]},
                    "$maxDistance": 50000  
                }
            }
        }
        matches_within_50km = list(collection.find(query_within_50km))

        ids_within_50km = [doc["_id"] for doc in matches_within_50km]


        query_outside_50km = {
            "blood_group": blood_group.upper(),
            "organ": organ.lower(),
            "_id": {"$nin": ids_within_50km}
        }
        matches_outside_50km = list(collection.find(query_outside_50km))

        combined = matches_within_50km + matches_outside_50km

        for doc in combined:
            doc["_id"] = str(doc["_id"])

        return {"matches": combined}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
