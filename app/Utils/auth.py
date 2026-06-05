from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from bson import ObjectId

from app.database.mongodb import database
from app.Utils.security import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login"
)

user_collection = database["users"]


def get_current_user(token: str = Depends(oauth2_scheme)):

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("user_id")

        if not user_id:
            raise HTTPException(
                status_code=401,
                detail="Invalid Token"
            )

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user = user_collection.find_one(
        {
            "_id": ObjectId(user_id)
        }
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    user["_id"] = str(user["_id"])

    if "password" in user:
        del user["password"]

    return user


def admin_required(
    current_user = Depends(get_current_user)
):

    if current_user["role"] != "Admin":

        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return current_user


def manager_or_admin_required(
    current_user = Depends(get_current_user)
):

    if current_user["role"] not in ["Admin", "Manager"]:

            raise HTTPException(
                status_code=403,
                detail="Manager or Admin access required"
            )
    return current_user


def cashier_or_admin_required(
    current_user = Depends(get_current_user)
):

    if current_user["role"] not in ["Admin", "Cashier"]:

        raise HTTPException(
            status_code=403,
            detail="Cashier or Admin access required"
        )

    return current_user


def kitchen_or_admin_required(
    current_user = Depends(get_current_user)
):

    if current_user["role"] not in ["Admin", "Kitchen"]:

        raise HTTPException(
            status_code=403,
            detail="Kitchen or Admin access required"
        )

    return current_user