from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from utils.auth import hash_password, verify_password, create_access_token, create_refresh_token
from utils.database import users_collection
from models import UserModel

auth_router = APIRouter()

@auth_router.post("/register")
async def register(user_name: str, user_email: str, mobile_number: str, password: str):
    if users_collection.find_one({"user_email": user_email}):
        raise HTTPException(status_code=400, detail="Email already registered.")
    hashed_password = hash_password(password)
    user = UserModel(user_name, user_email, mobile_number, hashed_password)
    users_collection.insert_one(user.__dict__)
    return {"message": "User registered successfully"}

@auth_router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_collection.find_one({"user_email": form_data.username})
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token({"user_id": user["user_id"]})
    refresh_token = create_refresh_token({"user_id": user["user_id"]})
    return {"access_token": access_token, "refresh_token": refresh_token}

@auth_router.post("/logout")
async def logout():
    return {"message": "Logout successful. Tokens should be cleared on the client side."}
