from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from routes.auth import router as auth_router
from routes.products import router as product_router
from routes.categories import router as category_router
from routes.promos import router as promo_router
from routes.banner import router as banner_router
from routes.medical import router as medical_router
from routes.cart import router as cart_router
from routes.pets import router as pet_router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(product_router, tags=["products"])
app.include_router(category_router, tags=["categories"])
app.include_router(promo_router, tags=["promos"])
app.include_router(banner_router, tags=["banners"])
app.include_router(medical_router, tags=["medicals"])
app.include_router(cart_router, tags=["cart"])
app.include_router(pet_router, tags=["pets"])

about_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Petify FastApi by Lihindu Perera</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f4f4f9;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            overflow: hidden;
        }

        .container {
            text-align: center;
            position: relative;
            animation: fadeIn 3s ease-out;
        }

        .title {
            font-size: 3em;
            font-weight: bold;
            color: #ff6347;
            letter-spacing: 2px;
            opacity: 0;
            animation: titleAnimation 2s forwards, typing 4s steps(20) 1s forwards;
            white-space: nowrap;
            overflow: hidden;
            display: inline-block;
            border-right: 4px solid #ff6347;
            padding-right: 5px;
        }

        .subtitle {
            font-size: 1.5em;
            color: #555;
            margin-top: 20px;
            opacity: 0;
            animation: subtitleAnimation 2s 1s forwards;
        }

        @keyframes fadeIn {
            0% {
                opacity: 0;
            }
            100% {
                opacity: 1;
            }
        }

        @keyframes titleAnimation {
            0% {
                opacity: 0;
                transform: translateY(-50px);
            }
            100% {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes subtitleAnimation {
            0% {
                opacity: 0;
                transform: translateY(50px);
            }
            100% {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes typing {
            0% {
                width: 0;
            }
            100% {
                width: 100%;
            }
        }

        .background {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: url('https://via.placeholder.com/1920x1080') no-repeat center center fixed;
            background-size: cover;
            filter: blur(8px);
            z-index: -1;
            animation: fadeIn 5s ease-out;
        }
    </style>
</head>
<body>
    <div class="background"></div>
    <div class="container">
        <div class="title">Petify FastApi</div>
        <div class="subtitle">by Lihindu Perera</div>
    </div>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def read_root():
    return about_html

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)
