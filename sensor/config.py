from dataclasses import dataclass
import pymongo
import os

MONGO_DB_URL_KEY = 'MONGO_DB_URL'

@dataclass
class EvironmentVariable:
    mongodb_url:str = os.getenv(MONGO_DB_URL_KEY)


my_env = EvironmentVariable()
mongo_client = pymongo.MongoClient(my_env.mongodb_url)
