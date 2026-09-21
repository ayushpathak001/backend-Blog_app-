from typing import Dict
import os

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from bson import ObjectId

from schemas import Token_data, db

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES" , ""))
SECRET_KEY = os.getenv("SECRET_KEY", "")
ALGORITHM = os.getenv("ALGORITHM", "")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(payload: Dict):
    to_encode = payload.copy()

    expiration_time = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expiration_time
    })

    return jwt.encode(
        to_encode,
        key=SECRET_KEY,
        algorithm=ALGORITHM
    )


def verify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(
            token,
            key=SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        id: str = payload.get("id")

        if not id:
            raise credential_exception

        token_data = Token_data(id=id)

        return token_data

    except JWTError:
        raise credential_exception


async def get_current_user(
    token: str = Depends(oauth2_scheme)
):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token could not be verified..",
        headers={"WWW-Authenticate": "Bearer"}
    )

    current_user_id = verify_access_token(
        token,
        credential_exception
    ).id

    current_user = await db["users"].find_one(
        {"_id": ObjectId(current_user_id)}
    )

    if current_user is None:
        raise credential_exception

    return current_user



async def get_user_from_reset_token(token: str):
    try:
        print("TOKEN RECEIVED:", token)
        print("SECRET KEY EXISTS:", bool(SECRET_KEY))
        print("ALGORITHM:", ALGORITHM)

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        print("DECODED PAYLOAD:", payload)

        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=401,
                detail="Invalid reset token: user ID missing"
            )

        return user_id

    except JWTError as e:
        print("JWT ERROR:", repr(e))

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired reset token"
        )



