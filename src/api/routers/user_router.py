# Third Party Imports
from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from models.user import User
from utils.database import create_user, fetch_users

router = APIRouter()


@router.post("/", response_description="User added into the database")
async def create_user_data(user: User = Body(...)) -> dict:
    """Creates a new user in the Mongo database.

    Args:
        user (User): The user object to be added to the database.

    Returns:
        The user created in the database.
    """
    user = jsonable_encoder(user)
    new_user = await create_user(user)
    return new_user


@router.get("/", response_description="Users retrieved")
async def get_users() -> list[dict]:
    """Fetches all the user from the Mongo database.

    Returns:
        A list of user in the database.
    """
    users = await fetch_users()
    return users
