from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor

client = MongoClient(
    "mongodb://localhost:27017",
    maxPoolSize = 50, # maximum these many connection can be created.
    minPoolSize = 10, # even when idle these many connection will be there
    serverSelectionTimeoutMS=5000 # if driver cannot connect to the server in 5 sec - it raises an error.
)

db = client.fastapi_db
executor = ThreadPoolExecutor(max_workers=10) # this will create 10 threads which will execute the tasks : these borrow the connection and does the transactions
