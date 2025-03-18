from pymongo import MongoClient
from config.uri import MongoClient as uri_connection

client = MongoClient(uri_connection)

user_db = client.user_db
user_collection = user_db["user_collection"]

shop_db = client.shop_db
product_collection = shop_db["shop_products"]