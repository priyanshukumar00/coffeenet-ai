from fastapi import APIRouter, Body, Depends
from bson import ObjectId
from typing import Optional

from app.database.mongodb import database
from app.schemas.user import UserCreate
from app.Utils.security import hash_password
from app.schemas.user import UserUpdate
from app.schemas.user import UserLogin
from app.Utils.security import verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from app.Utils.auth import admin_required as admin
from app.Utils.auth import get_current_user

router = APIRouter()

user_collection = database["users"]

@router.post("/users")
def create_user(user: UserCreate, current_user = Depends(admin)):

    existing_user = user_collection.find_one(
        {
            "email": user.email
        }
    )

    if existing_user:

        return {
            "message":
            "Email already registered"
        }

    user_dict = user.model_dump()

    user_dict["password"] = hash_password(
        user.password
    )

    result = user_collection.insert_one(
        user_dict
    )

    user_dict["_id"] = str(
        result.inserted_id
    )

    del user_dict["password"]

    return {
        "message":
        "User created successfully",
        "data":
        user_dict
    }


#------- Get All Users ----------------
@router.get("/users")
def get_users(
    page: int = 1,
    limit: int = 10,
    role: Optional[str] = None,
    current_user = Depends(admin)
):

    if page < 1:
        return {
            "message": "Page must be greater than 0"
        }

    if limit < 1 or limit > 100:
        return {
            "message": "Limit must be between 1 and 100"
        }

    query = {}

    if role:
        allowed_roles = [
            "Admin",
            "Manager",
            "Cashier",
            "Kitchen"
        ]

        if role not in allowed_roles:
            return {
                "message": "Invalid user role"
            }

        query["role"] = role

    users = []

    skip = (page - 1) * limit

    for user in user_collection.find(query).skip(skip).limit(limit):

        user["_id"] = str(user["_id"])

        if "password" in user:
            del user["password"]

        users.append(user)

    total_users = user_collection.count_documents(query)

    return {
        "page": page,
        "limit": limit,
        "total_users": total_users,
        "users": users
    }


@router.get("/users/{user_id}")
def get_user(user_id: str, current_user = Depends(admin)):

    if not ObjectId.is_valid(user_id):
        return {
            "message": "Invalid user id"
        }

    user = user_collection.find_one(
        {
            "_id": ObjectId(user_id)
        }
    )

    if not user:
        return {
            "message": "User not found"
        }

    user["_id"] = str(user["_id"])

    if "password" in user:
        del user["password"]

    return {
        "message": "User fetched successfully",
        "data": user
    }



#------ 
@router.put("/users/{user_id}")
def update_user(
    user_id: str,
    user: UserUpdate,
    current_user = Depends(admin)
):

    if not ObjectId.is_valid(user_id):

        return {
            "message":
            "Invalid user id"
        }

    existing_user = user_collection.find_one(
        {
            "_id": ObjectId(user_id)
        }
    )

    if not existing_user:

        return {
            "message":
            "User not found"
        }

    update_data = user.model_dump(
        exclude_unset=True
    )

    if not update_data:

        return {
            "message":
            "No data provided for update"
        }

    if "email" in update_data:

        duplicate_user = user_collection.find_one(
            {
                "email": update_data["email"],
                "_id": {
                    "$ne": ObjectId(user_id)
                }
            }
        )

        if duplicate_user:

            return {
                "message":
                "Email already registered"
            }

    if "password" in update_data:

        update_data["password"] = hash_password(
            update_data["password"]
        )

    user_collection.update_one(
        {
            "_id": ObjectId(user_id)
        },
        {
            "$set": update_data
        }
    )

    return {
        "message":
        "User updated successfully"
    }


# ----- Delete Single
@router.delete("/users/{user_id}")
def delete_user(user_id: str, current_user = Depends(admin)):

    if not ObjectId.is_valid(user_id):

        return {
            "message":
            "Invalid user id"
        }

    existing_user = user_collection.find_one(
        {
            "_id": ObjectId(user_id)
        }
    )

    if not existing_user:

        return {
            "message":
            "User not found"
        }

    user_collection.delete_one(
        {
            "_id": ObjectId(user_id)
        }
    )

    return {
        "message":
        "User deleted successfully"
    }


#--------- Delete Multiple
@router.delete("/users")
def delete_users(ids: list[str] = Body(...), current_user = Depends(admin)):

    if not ids:

        return {
            "message":
            "Please provide at least one user id"
        }

    object_ids = []

    for user_id in ids:

        if not ObjectId.is_valid(user_id):

            return {
                "message":
                f"{user_id} is not a valid user id"
            }

        object_ids.append(
            ObjectId(user_id)
        )

    existing_count = user_collection.count_documents(
        {
            "_id": {
                "$in": object_ids
            }
        }
    )

    if existing_count == 0:

        return {
            "message":
            "No matching users found"
        }

    result = user_collection.delete_many(
        {
            "_id": {
                "$in": object_ids
            }
        }
    )

    return {
        "message":
        f"{result.deleted_count} user(s) deleted successfully"
    }


#---------- Login API
@router.post("/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends()
):

    existing_user = user_collection.find_one(
        {
            "email": form_data.username
        }
    )

    if not existing_user:
        return {
            "message": "Invalid email or password"
        }

    password_valid = verify_password(
        form_data.password,
        existing_user["password"]
    )

    if not password_valid:
        return {
            "message": "Invalid email or password"
        }

    access_token = create_access_token(
        {
            "user_id": str(existing_user["_id"]),
            "email": existing_user["email"],
            "role": existing_user["role"]
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/me")
def get_logged_in_user(
    current_user = Depends(get_current_user)
):

    return {
        "message": "Logged in user fetched successfully",
        "data": current_user
    }