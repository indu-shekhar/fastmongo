from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserCreate(BaseModel):
    """
    UserCreate model for validating user creation requests.

    This Pydantic model defines the schema for creating a new user with the following fields:

    Attributes:
        name (str): The user's name. Must be at least 2 characters long.
            The '...' (Ellipsis) means this field is required with no default value.
        email (EmailStr): The user's email address in a valid email format.
            This field is required.
        age (int): The user's age. Must be between 1 and 120 (inclusive).
            The '...' (Ellipsis) means this field is required with no default value.

    Note:
        The '...' (Ellipsis) in Pydantic's Field() function indicates that a field is required
        and has no default value. If not provided during instantiation, validation will fail.
    """
    name: str = Field(..., min_length=2)
    email: EmailStr = Field(...)
    age: int = Field(..., ge=1, le=120)


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2)
    age: Optional[int] = Field(None, ge=1, le=120)

class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    age: int
