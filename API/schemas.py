import motor.motor_asyncio
from dotenv import load_dotenv
import os
from bson import ObjectId

from typing import Any
from pydantic import BaseModel, Field, EmailStr, ConfigDict, GetCoreSchemaHandler
from pydantic_core import core_schema


load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URI)

db = client.BLOG_API


# BSON AND FASTAPI JSON

class PyObjectId(ObjectId):

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,
        handler: GetCoreSchemaHandler
    ):
        return core_schema.no_info_plain_validator_function(
            cls.validate,
            serialization=core_schema.to_string_ser_schema()
        )

    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return v

        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")

        return ObjectId(v)


class User(BaseModel):
    name: str
    email: EmailStr
    password: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "John Doe",
                "email": "john@example.com",
                "password": "your_secret"
            }
        }
    )



class UserResponse(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    email: EmailStr


    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "_id": "507f1f77bcf86cd799439011",
                "name": "John Doe",
                "email": "john@example.com"
            }
        }
    )





class Token_data(BaseModel):
    id : str 


class PasswordReset(BaseModel):
    email : EmailStr


class NewPassword(BaseModel):
    password : str



class BlogContentResponse(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title : str = Field(...)
    body : str = Field(...)
    author_name : str = Field(...)
    author_id : str = Field(...)
    created_at : str = Field(...)

    model_config = ConfigDict(
            populate_by_name=True,
            arbitrary_types_allowed=True,
            json_schema_extra={
                "example": {
                    "title": "Blog title",
                    "body": "body content" , 
                    "author_name" : "name of the author" ,
                    "author_id" : "id of the author" ,
                    "created_at" : "date when it created"
                }
            }
        )


    

class BlogContent(BaseModel):
    title: str
    body: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Blog title",
                "body": "body content"
            }
        }
    )