from pymongo import MongoClient
from config.uri import MongoClient as uri_connection

client = MongoClient(uri_connection)

db = client.todo_db

collection_name = db["todo_collection"]