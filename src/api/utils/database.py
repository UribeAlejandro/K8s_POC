# Standard Library Imports
import asyncio
import os

# Third Party Imports
from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.collection import Collection

# docformatter Local Imports
from .helpers import user_helper


def mongo_connect() -> Collection:
    """Connects to a MongoDB instance returning a Collection instance.

    Returns:
        A MongoDB collection object.
    """
    host = f"mongodb://{os.environ['MONGO_HOST']}"
    client = AsyncIOMotorClient(host=host)
    client.get_io_loop = asyncio.get_event_loop
    database = client.users
    collection = database.get_collection("users_collection")

    return collection


users_collection = mongo_connect()


async def fetch_users() -> list[dict]:
    """Fetches asynchronously all users from a MongoDB Collection.

    Returns:
        A list of user from the collection.
    """
    users = [user_helper(users) async for users in users_collection.find()]
    return users


async def create_user(user_data: dict) -> dict:
    """Inserts asynchronously a user into the MongoDB collection.

    Args:
        user_data (dict): A dictionary with the user information.

    Returns:
        A dictionary with the user information fetched from the database as a dictionary.
    """
    user = await users_collection.insert_one(user_data)
    new_user = await users_collection.find_one({"_id": user.inserted_id})
    return user_helper(new_user)


async def fetch_user(user_id: str) -> dict:
    """Fetches asynchronously a user from th MongoDB by id.

    Args:
        user_id (str): The user id in the database.

    Returns:
        A dictionary with the user information fetched from the database.
    """
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return user_helper(user)


async def update_user(user_id: str, user_data: dict) -> bool:
    """Updates asynchronously a user in the MongoDB collection. Needs the user
    id and a dictionary of user properties to update.

    Args:
        user_id (str): The user id in the database.
        user_data (dict): A dictionary containing the user information to be updated into the database.

    Returns:
        A boolean value indicating if the user update was successful.
    """
    # Return false if an empty request body is sent.
    if not user_data:
        return False

    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        updated_user = await users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": user_data})
        if updated_user:
            return True
        return False


async def delete_user(user_id: str) -> bool:
    """`   Deletes asynchronously a user from the MongoDB collection. Needs the
    user id of the user to be removed.

    Args:
        user_id (str): The user id in the database.

    Returns:
        A boolean indicating if the deletion of the user from the database was successful.
    """
    user = await users_collection.find_one({"_id": ObjectId(user_id)})

    if user:
        await users_collection.delete_one({"_id": ObjectId(user_id)})
        return True
    else:
        return False
