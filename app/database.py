from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor

client = MongoClient(
    "mongodb://localhost:27017",
    maxPoolSize = 50, # maximum these many connection can be created.
    minPoolSize = 10, # even when idle these many connection will be there
    serverSelectionTimeoutMS=5000 # if the driver cannot connect to the server within 5 seconds, it will time out and raise an exception during server selection.
)

db = client.fastapi_db
executor = ThreadPoolExecutor(max_workers=10) # this will create 10 threads which will execute the tasks : these borrow the connection and do the transactions
