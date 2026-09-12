from fastapi import APIRouter, HTTPException , status
from schemas import User , db , UserResponse
from fastapi.encoders import jsonable_encoder
from utils import get_password_hash
import secrets
from send_email import send_registeration_mail

router = APIRouter(
    tags= ["Register user"]
)






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

    try:
        await send_registeration_mail(
            subject="Welcome to My Blog 🎉",
            email_to=created_user["email"],
            body={
                "name": created_user["name"],
                "email": created_user["email"],
            }
        )
    except Exception as e:
        print("Email sending failed:", e)

    return created_user



