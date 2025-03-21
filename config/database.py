from pymongo import MongoClient
from config.uri import MongoClient as uri_connection

client = MongoClient(uri_connection)

# Shop  --->>>
shop_products = client.shop_db
product_collection = shop_products["shop_products"]

shop_categories = client.shop_db
category_collection = shop_categories["shop_categories"]

shop_promos = client.shop_db
promo_collection = shop_promos["shop_promos"]

shop_banners = client.shop_db
banner_collection = shop_banners["shop_banners"]

# User --->>>
user_db = client.user_db
user_collection = user_db["user_collection"]

# Medicals --->>>
medicals = client.medical_db
medical_collection = medicals["medicals"]

# Pets --->>>
pets = client.pet_db
pet_collection = pets["pets"]