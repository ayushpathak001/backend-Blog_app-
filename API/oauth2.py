from typing import Dict
import os

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from bson import ObjectId

from schemas import Token_data, db

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "")
)

SECRET_KEY = os.getenv("SECRET_KEY", "")
ALGORITHM = os.getenv("ALGORITHM", "")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(payload: Dict):
    to_encode = payload.copy()

    expiration_time = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expiration_time.timestamp()
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

    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired reset token"
    )

    try:

        payload = jwt.decode(
            token,
            key=SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("id")

        if not user_id:
            raise credential_exception

        user = await db["users"].find_one(
            {"_id": ObjectId(user_id)}
        )

        if user is None:
            raise credential_exception

        return user

    except JWTError as e:
        print("jwt error" , e)
        raise credential_exception

    except Exception as e:
        print("RESET TOKEN ERROR:", e)
        raise credential_exception