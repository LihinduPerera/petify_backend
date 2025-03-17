from fastapi import APIRouter, HTTPException, Depends
from schema.user import UserIn, UserOut, UserLogin
from config.database import user_collection
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
SECRET_KEY = "lihindu_perera"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
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

@router.post("/register", response_model=UserOut)
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
    return UserOut(name=user_in.name, email=user_in.email, address=user_in.address, phone=user_in.phone)

@router.post("/login")
async def login(user_in: UserLogin):
    user = user_collection.find_one({"email": user_in.email})
    if not user or not verify_password(user_in.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid Credentials !!")
    access_token = create_access_token(data={"sub": user_in.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/current-user", response_model=UserOut)
async def get_user_data(current_user: dict = Depends(get_current_user)):
    return {"name": current_user["name"], "email": current_user["email"], "address": current_user["address"], "phone": current_user["phone"]}

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
