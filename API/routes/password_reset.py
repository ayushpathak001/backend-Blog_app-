from fastapi import APIRouter, HTTPException , status
from utils import get_password_hash
from oauth2 import create_access_token, get_user_from_reset_token
from schemas import NewPassword, PasswordReset , db
from send_email import password_reset


router = APIRouter(
    prefix="/password" , 
    tags=["Password Reset"]
)

@router.post("" , response_description="Reset Password")
async def reset_request(user_email : PasswordReset ):
    user = await db["users"].find_one({"email" :user_email.email})

    if user is not None:
        token = create_access_token({"id" : str(user["_id"])})

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
    new_passsword: NewPassword
):

    user = await get_user_from_reset_token(token)

    request_data = {
        k: v
        for k, v in new_passsword.dict().items()
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

        updated_user = await db["users"].find_one(
            {"_id": user["_id"]}
        )

        return updated_user

    raise HTTPException(
        status_code=404,
        detail="User information not found on the server"
    )




    