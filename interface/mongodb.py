#connect to MongoDB
import asyncio
import motor.motor_asyncio
from utils import env_config

client = motor.motor_asyncio.AsyncIOMotorClient(env_config.MONGO_CONN_STR)
client.get_io_loop = asyncio.get_running_loop

class MongoInterface:
    def __init__(self):
        self.db = self.client['test']
        self.collection = self.db['test']

    def insert(self, data):
        self.collection.insert_one(data)

    def find(self, data):
        return self.collection.find_one(data)

    def delete(self, data):
        self.collection.delete_one(data)

    def update(self, data, newdata):
        self.collection.update_one(data, newdata)

    def close(self):
        self.client.close()