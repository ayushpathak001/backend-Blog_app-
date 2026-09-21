from fastapi import APIRouter, HTTPException , status
from utils import get_password_hash
from oauth2 import create_access_token, get_user_from_reset_token
from oauth2 import create_access_token, get_user_from_reset_token
from schemas import NewPassword, PasswordReset , db
from send_email import password_reset
from bson import ObjectId
from fastapi import HTTPException


router = APIRouter(
    prefix="/password" , 
    tags=["Password Reset"]
)

@router.post("" , response_description="Reset Password")
async def reset_request(user_email : PasswordReset ):
    user = await db["users"].find_one({"email" :user_email.email})

    if user is not None:
        token = create_access_token({"sub": str(user["_id"])})

        reset_link = f"http://localhost:8000/?token={token}"

        # Todo : send email
        await password_reset("Password Reset" , user["email"] , body={
            "title" : "Password Reset" , 
            "name" : user["name"],
            "email" : user["email"] , 
            "reset_link" : reset_link
            }
        )



    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND , 
            detail= "user with this email not found.."
        )




@router.post("/reset", response_description="Reset Password")
async def reset(
    token: str,
    new_password: NewPassword
):
    user_id = await get_user_from_reset_token(token)

    try:
        user_object_id = ObjectId(user_id)
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid reset token"
        )

    user = await db["users"].find_one(
        {"_id": user_object_id}
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    request_data = {
        k: v
        for k, v in new_password.dict().items()
        if v is not None
    }

    if "password" in request_data:
        request_data["password"] = get_password_hash(
            request_data["password"]
        )

    update_result = await db["users"].update_one(
        {"_id": user["_id"]},
        {"$set": request_data}
    )

    if update_result.modified_count == 1:
        return { "message": "Password reset successfully" }

        

    raise HTTPException( status_code=400, detail="Password was not changed" )

