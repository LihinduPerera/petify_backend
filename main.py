from fastapi import FastAPI
from routes.auth import router as auth_router
from routes.products import router as product_router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(product_router , tags=["products"])

@app.get("/")
def read_root():
    return {"message": "Welcome to PETIFY fastAPI"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)