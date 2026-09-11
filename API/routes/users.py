from fastapi import APIRouter, HTTPException , status
from schemas import User , db , UserResponse
from fastapi.encoders import jsonable_encoder
from utils import get_password_hash
import secrets


router = APIRouter(
    tags= ["User Routes"]
)




@router.get("/")
def read_root():
    return {
        "Hello" : "World.."
    }


@router.post(
    "/registration",
    response_description="Register a user",
    response_model=UserResponse
)
async def register(user_info: User):

    user_info = jsonable_encoder(user_info)

    username_found = await db["users"].find_one(
        {"name": user_info["name"]}
    )

    email_found = await db["users"].find_one(
        {"email": user_info["email"]}
    )

    if username_found:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="username is already taken.."
        )

    if email_found:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="email is already taken..."
        )

    user_info["password"] = get_password_hash(
        user_info["password"]
    )

    user_info["apiKey"] = secrets.token_hex(30)

    new_user = await db["users"].insert_one(user_info)

    created_user = await db["users"].find_one(
        {"_id": new_user.inserted_id}
    )

    return created_user





@router.get("/test-db")
async def test_db():
    try:
        result = await db.command("ping")
        return {"message": "MongoDB connected", "result": result}
    except Exception as e:
        return {"message": "MongoDB connection failed", "error": str(e)}