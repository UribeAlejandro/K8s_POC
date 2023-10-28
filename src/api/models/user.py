# Standard Library Imports
from typing import Optional

# Third Party Imports
from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    """Class defining the user model in the database."""

    name: str = Field(...)
    last_name: str = Field(...)
    email: EmailStr = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "name": "Bob",
                "last_name": "Smith",
                "email": "bob.smith@example.com",
            }
        }


class UpdateUser(BaseModel):
    """Class defining the model to update a user in the database."""

    name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]

    class Config:
        schema_extra = {
            "example": {
                "name": "Bob",
                "last_name": "smith",
                "email": "bob.smith@example.com",
            }
        }
