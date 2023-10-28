# Standard Library Imports
import os
from functools import wraps
from typing import Any, Callable

# Third Party Imports
import requests
from fastapi import HTTPException


def user_helper(user: dict) -> dict:
    """Parses the object dictionary received from the MongoDB connector as a
    dictionary.

    Args:
        user (dict): the user dictionary fetched from the database.

    Returns:
        A dictionary with the user properties.
    """
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "last_name": user["last_name"],
        "email": user["email"],
    }


def auth_required(func: Callable) -> Callable:
    """Decorator to enable authentication through an external service via an
    authorization header.

    Args:
        func (Callable): Python callable to decorate.

    Returns:
        An asynchronous wrapper decorating the callable.
    """
    auth_host = os.environ["AUTH_SERVICE_HOST"]
    endpoint = "auth"

    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Callable:
        """Function wrapper to decorate callables calling  via an HTTP request
        the external authentication service.

        Args:
            *args : Decorated callable args.
            **kwargs : Decorated callable kwargs.

        Returns:
            If it receives a 2xx HTTP response returns the decorated callable. If it receives an HTTP error
            raises a 401 HTTP unauthorized code.
        """
        try:
            response = requests.post(
                url=f"http://{auth_host}/{endpoint}",
                headers={
                    "Authorization": kwargs["authorization"],
                },
            )
            response.raise_for_status()
            return await func(*args, **kwargs)
        except requests.HTTPError:
            raise HTTPException(status_code=401, detail="Unauthorized")

    return wrapper
