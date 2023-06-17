from datetime import datetime
from typing import Optional

from bson.objectid import ObjectId
from fastapi import HTTPException
from pymongo.database import Database

from ..utils.security import hash_password


class AuthRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_user(self, user: dict):
        payload = {
            "email": user["email"],
            "password": hash_password(user["password"]),
            "created_at": datetime.utcnow(),
        }

        self.database["users"].insert_one(payload)

    def get_user_by_id(self, user_id: str) -> Optional[dict]:
        user = self.database["users"].find_one(
            {
                "_id": ObjectId(user_id),
            }
        )
        return user

    def get_user_by_email(self, email: str) -> Optional[dict]:
        user = self.database["users"].find_one(
            {
                "email": email,
            }
        )
        return user

    def update_user(self, user_id: str, data: dict):
        self.database["users"].update_one(
            filter={"_id": ObjectId(user_id)},
            update={
                "$set": {
                    "phone": data["phone"],
                    "name": data["name"],
                    "city": data["city"],
                }
            },
        )

    def add_to_favourites(self, user_id: str, shanyrak: dict):
        self.database['users'].update_one(
            filter={"_id": ObjectId(user_id)},
            update={
                "$push": {
                    "shanyraks": shanyrak
                }
            },
        )

    def get_user_favourites(self, user_id: str) -> list:
        user = self.database["users"].find_one(
            {
                "_id": ObjectId(user_id),
            }
        )
        return user["shanyraks"] if user["shanyraks"] else []

    def delete_user_favourite(self, user_id: str, shanyrak_id: str):
        snanyrak_checker = self.database['users'].find_one(
            filter={
                "shanyraks._id": ObjectId(shanyrak_id)
            }
        )
        if snanyrak_checker:
            response = self.database['users'].update_one(
                filter={"_id": ObjectId(user_id)},
                update={
                    "$pull": {
                        "shanyraks": {
                            "_id": ObjectId(shanyrak_id)
                        }
                    }
                }
            )
            return response
        else:
            raise HTTPException(status_code=404, detail="Such favourite not found")
    
    def upload_avatar(self, user_id: str, avatar_url: str):
        user = self.database["users"].find_one(
            {
                "_id": ObjectId(user_id),
            }
        )
        if user['avatar_url']:
            self.database["users"].update_one(
                filter={"_id": ObjectId(user_id)},
                update={
                    {"$set": {"avatar_url": avatar_url}}
                }
            )

    def delete_avatar(self, user_id: str):
        user = self.database["users"].find_one(
            {
                "_id": ObjectId(user_id),
            }
        )
        if user['avatar_url']:
            self.database["users"].update_one(
                filter={"_id": ObjectId(user_id)},
                update={
                    {"$set": {"avatar_url": ""}}
                }
            )
        else:
            raise HTTPException(status_code=404, detail="Such avatar not found")
                