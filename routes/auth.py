from fastapi import APIRouter, HTTPException, Depends , Query
from models.user_model import UserIn, UserOut, UserLogin , UserUpdate ,ReadUsers , User ,AdminLogin
from config.database import user_collection , admin_collection
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from bson import ObjectId
from typing import List

router = APIRouter()
SECRET_KEY = "lihindu_perera"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 7
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(user: dict, expires_delta: timedelta = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)):
    to_encode = user.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        user = user_collection.find_one({"email": email})
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Token is invalid")
    
def str_id(id: ObjectId) -> str:
    return str(id)

@router.get("/users", response_model=list[ReadUsers])
async def get_users():
    users = user_collection.find() 
    if not users:
        raise HTTPException(status_code=404, detail="No users found")

    user_list = []
    for user in users:
        user_data = ReadUsers(
            id=str(user["_id"]),
            name=user["name"],
            email=user["email"],
            phone=user.get("phone", "")
        )
        user_list.append(user_data)

    return user_list

@router.get("/users/search/", response_model=List[ReadUsers])
async def search_user_by_email(query: str = Query(..., min_length=1, max_length=100)):
    users = []
    for user in user_collection.find({"email": {"$regex": query, "$options": "i"}}):
        users.append(ReadUsers(
            id=str(user["_id"]),
            name=user["name"],
            email=user["email"],
            phone=user.get("phone", "")
        ))
    return users

@router.post("/googleauth")
async def google_auth(User: User):
    user = {
        "name": User.name,
        "email": User.email,
        "address": User.address,
        "phone": User.phone
    }

    existing_user = user_collection.find_one({"email": User.email})
    if existing_user:
        existing_user_data = {
            "sub": User.email,
            "name": existing_user["name"],
            "email": existing_user["email"],
            "phone": existing_user.get("phone", ""),
            "address": existing_user.get("address", ""),
            "user_id": str(existing_user["_id"])
        }
        access_token = create_access_token(user=existing_user_data)
        return {"access_token": access_token, "token_type": "bearer", **existing_user_data}
    else: 
        result = user_collection.insert_one(user)
        user_id = str(result.inserted_id)

        created_user_data = {
            "sub": User.email,
            "name": User.name,
            "email": User.email,
            "phone": User.phone,
            "address": User.address,
            "user_id": user_id
        }
        access_token = create_access_token(user=created_user_data)
        return {"access_token": access_token, "token_type": "bearer", **created_user_data}

@router.post("/register")
async def register_user(user_in: UserIn):
    hashed_password = hash_password(user_in.password)
    user = {
        "name": user_in.name,
        "email": user_in.email,
        "address": user_in.address,
        "phone": user_in.phone,
        "password": hashed_password
    }

    existing_user = user_collection.find_one({"email": user_in.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    result = user_collection.insert_one(user)
    user_id = str(result.inserted_id)
    
    user_data = {
        "sub": user_in.email,
        "name": user_in.name,
        "email": user_in.email,
        "phone": user.get("phone", ""),
        "address": user.get("address", ""),
        "user_id": user_id,
    }

    access_token = create_access_token(user=user_data)
    return {"access_token": access_token, "token_type": "bearer", **user_data}

@router.post("/login")
async def login(user_in: UserLogin):
    user = user_collection.find_one({"email": user_in.email})
    if not user or not verify_password(user_in.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid Credentials !!")
    
    user_data = {
        "sub": user_in.email,
        "name": user["name"],
        "email": user["email"],
        "phone": user.get("phone", ""),
        "address": user.get("address", ""),
        "user_id": str(user["_id"])
    }

    access_token = create_access_token(user=user_data)
    return {"access_token": access_token, "token_type": "bearer",**user_data}

@router.put("/update-user", response_model=UserOut)
async def update_user(user_in: UserUpdate, current_user: dict = Depends(get_current_user)):
    user_id = current_user["_id"]
    
    updated_data = {}
    if user_in.name:
        updated_data["name"] = user_in.name
    if user_in.address is not None:
        updated_data["address"] = user_in.address
    if user_in.phone is not None:
        updated_data["phone"] = user_in.phone
    
    if not updated_data:
        raise HTTPException(status_code=400, detail="No data provided for update")

    result = user_collection.update_one({"_id": ObjectId(user_id)}, {"$set": updated_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    updated_user = user_collection.find_one({"_id": ObjectId(user_id)})
    
    return UserOut(
        name=updated_user["name"],
        email=updated_user["email"],
        address=updated_user.get("address"),
        phone=updated_user.get("phone")
    )

@router.post("/logout")
async def logout():
    return {"message": "Logged out successfully"}

@router.post("/reset-password")
async def reset_password(email: str):
    user = user_collection.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Send a reset link via email (this part is not implemented yet)
    return {"message": "Password reset email sent!! (Still not added this feature)"}

@router.get("/user-count")
async def get_user_count():
    count = user_collection.count_documents({})
    return {"user_count": count}

@router.post("/admin-login")
async def admin_login(admin_in: AdminLogin):
    admin = admin_collection.find_one({"email": admin_in.email})
    if not admin or not verify_password(admin_in.password, admin["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"message": "Login successful"}

@router.post("/admin-register")
async def admin_register(admin_in: AdminLogin):
    existing_admin = admin_collection.find_one({"email": admin_in.email})
    if existing_admin:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(admin_in.password)
    admin = {
        "email": admin_in.email,
        "password": hashed_password,
    }
    result = admin_collection.insert_one(admin)

    return {"message": "Registration successful"}