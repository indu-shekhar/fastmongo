from bson import ObjectId
from app.database import db
from app.utils.db_executor import run_db


async def create_user(data: dict):
    def create():
        return db.users.insert_one(data).inserted_id

    return await run_db(create)


async def get_user(user_id: str):
    def get():
        return db.users.find_one({"_id": ObjectId(user_id)})

    return await run_db(get)


async def list_users():
    def _list():
        return list(db.users.find())

    return await run_db(_list)


async def update_user(user_id: str, data: dict):
    def _update():
        return db.users.update_one({"_id": ObjectId(user_id)}, {"$set": data})

    return await run_db(_update)


async def delete_user(user_id: str):
    def _delete():
        return db.users.delete_one({"_id": ObjectId(user_id)})

    return await run_db(_delete)
