from typing import Any, List
from bson.objectid import ObjectId
from datetime import datetime
from fastapi import HTTPException
from pymongo.database import Database


class ShanyrakRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_shanyrak(self, user_id: str, data: dict[str, Any]):
        data["user_id"] = ObjectId(user_id)
        insert_result = self.database["shanyraks"].insert_one(data)
        return insert_result.inserted_id

    def get_shanyrak(self, shanyrak_id: str):
        return self.database["shanyraks"].find_one({"_id": ObjectId(shanyrak_id)})

    def get_my_shanyraks(self, user_id: str) -> List[dict]:
        shanyraks = self.database['shanyraks'].find(
            {
                'user_id': ObjectId(user_id)
            }
        )
        result = []
        for shanyrak in shanyraks:
            result.append(shanyrak)
        return result

    def update_shanyrak(
        self, shanyrak_id: str, user_id: str, data: dict[str, Any]
    ):
        return self.database["shanyraks"].update_one(
            filter={"_id": ObjectId(shanyrak_id), "user_id": ObjectId(user_id)},
            update={
                "$set": data,
            },
        )

    def delete_shanyrak(self, shanyrak_id: str, user_id: str):
        return self.database["shanyraks"].delete_one(
            {"_id": ObjectId(shanyrak_id), "user_id": ObjectId(user_id)}
        )
    
    def create_comment_by_id(self, id: str, user_id: str, content: str):
        comment_id = ObjectId()  # Generate a random comment ID
        created_at = datetime.now()  # Get the current timestamp
        shanyrak_checker = self.database["shanyraks"].find_one({"_id": ObjectId(id)})
        if shanyrak_checker:
            comment = {
                "_id": comment_id,
                "author_id": ObjectId(user_id),
                "content": content,
                "created_at": created_at
            }
            self.database["shanyraks"].update_one(
                filter={"_id": ObjectId(id)},
                update={
                    "$push": {"comments": comment}
                }
            )
        else:
            raise HTTPException(
                status_code=404,
                detail="Shanyrak not found",
            )
        
    def get_comments_by_id(self, shanyrak_id: str):
        shanyrak = self.database["shanyraks"].find_one({"_id": ObjectId(shanyrak_id)})
        if shanyrak is None:
            raise HTTPException(status_code=404, detail="Shanyrak not found")
        comments = shanyrak.get("comments", [])
        return comments
    
    def update_comment_by_id(self, user_id: str, 
                             shanyrak_id: str, comment_id: str, updated_content: str
    ):
        result = self.database["shanyraks"].update_one(
            filter={
                "_id": ObjectId(shanyrak_id),
                "comments": {
                    "$elemMatch": {
                        "_id": ObjectId(comment_id),
                        "author_id": ObjectId(user_id)
                    }
                }
            },
            update={
                "$set": {
                    "comments.$.content": updated_content
                }
            }
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Shanyrak or comment not found")
        elif result.modified_count == 0:
            raise HTTPException(status_code=403, detail="You are not allowed to update this comment")

    def delete_comment_by_id(
        self, user_id: str, shanyrak_id: str, comment_id: str
    ):
        result = self.database["shanyraks"].update_one(
            filter={
                "_id": ObjectId(shanyrak_id),
                "comments": {
                    "$elemMatch": {
                        "_id": ObjectId(comment_id),
                        "author_id": ObjectId(user_id)
                    }
                }
            },
            update={
                "$pull": {
                    "comments": {
                        "_id": ObjectId(comment_id)
                    }
                }
            }
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Shanyrak or comment not found")
        elif result.modified_count == 0:
            raise HTTPException(status_code=403, detail="You are not allowed to delete this comment")

    def upload_images(self, id: str, user_id: str, image_url: str):
        check_shanyrak_exist = self.database["shanyraks"].find_one(
            {"$and": [{"_id": ObjectId(id)}, {"author_id": ObjectId(user_id)}]}
        )
        if check_shanyrak_exist:
            self.database["shanyraks"].update_one(
                {"$and": [{"_id": ObjectId(id)}, {"author_id": ObjectId(user_id)}]},
                {"$push": {"media": image_url}},
            )
        else:
            raise HTTPException(
                status_code=404,
                detail="Shanyrak does not exist, or you cannot upload images to others posts",)
        
    def delete_images(self, id: str, user_id: str, image_url: str):
        check_shanyrak_exist = self.database["shanyraks"].find_one(
            {"$and": [{"_id": ObjectId(id)}, {"author_id": ObjectId(user_id)}]}
        )
        if check_shanyrak_exist:
            self.database["shanyraks"].update_one(
                {"$and": [{"_id": ObjectId(id)}, {"author_id": ObjectId(user_id)}]},
                {"$pull": {"media": image_url}},
            )
        else:
            raise HTTPException(
                status_code=404,
                detail="Shanyrak does not exist, or you cannot upload images to others posts",)
        
    def get_filtered_shanyraks(
        self,
        limit: int,
        offset: int,
        type: str | None,
        rooms_count: int | None,
        price_from: int | None,
        price_until: int | None,
        latitude: float | None,
        longitude: float | None,
        radius: float | None,
    ):
        def get_query_filter(
            query_filter: dict,
            type: str | None,
            rooms_count: int | None,
            price_from: int | None,
            price_until: int | None,
            latitude: float | None,
            longitude: float | None,
            radius: float | None,
        ):
            if type is not None:
                query_filter["type"] = type
            if rooms_count is not None:
                query_filter["rooms_count"] = rooms_count
            price_filter = {}
            if price_from is not None:
                price_filter["$gte"] = price_from
            if price_until is not None:
                price_filter["$lte"] = price_until
            if price_filter != {}:
                query_filter["price"] = (price_filter,)
            if latitude is not None and longitude is not None and radius is not None:
                radius_converted_approximately = radius * 3.2535313808
                query_filter["location"] = {
                    "$geoWithin": {
                        "$centerSphere": [
                            [longitude, latitude],
                            radius_converted_approximately,
                        ]
                    }
                }
            return query_filter

        response_count = 0
        query_filter = get_query_filter(
            {},
            type,
            rooms_count,
            price_from,
            price_until,
            latitude,
            longitude,
            radius,
        )
        if limit == 0 and offset == 0:
            response = self.database["shanyraks"].find(query_filter)
            response_count = self.database["shanyraks"].count_documents({})
        else:
            response = (
                self.database["shanyraks"].find(query_filter).limit(limit).skip(offset)
            )

            response_count = self.database["shanyraks"].count_documents(query_filter)

        response_list = []
        for shanyrak in response:
            response_list.append(
                {
                    "_id": str(shanyrak["_id"]),
                    "type": shanyrak["type"],
                    "rooms_count": shanyrak["rooms_count"],
                    "address": shanyrak["address"],
                    "price": shanyrak["price"],
                    "area": shanyrak["area"],
                    "location": shanyrak["location"],
                }
            )
        return {"total": response_count, "items": response_list}