#connect to MongoDB
import asyncio
import motor.motor_asyncio
from bson import ObjectId
from app.utils import env_config
from app.utils.logger import init_logger

logger = init_logger(__name__)

client = motor.motor_asyncio.AsyncIOMotorClient(env_config.MONGO_CONN_STR)
client.get_io_loop = asyncio.get_running_loop

class MongoInterface:

    def __init__(self, collection_name: str, c_database=None, index_list=[]):
        if c_database is None:
            c_database = client[env_config.MONGO_DB_NAME]
        self.collection = c_database[collection_name]
        if index_list:
            logger.info("Creating index for collection: %s list %s",
                        collection_name,
                        index_list)
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.set_index(index_list))

    async def set_collection(self, collection_name: str):
        """
        Set collection name.
        input: collection name
        """
        self.collection = client[env_config.MONGO_DB_NAME][collection_name]

    async def get_collection_object(self):
        """
        Get the collection object.
        Can be used to do custom operations on modules.
        return: collection object
        """
        return self.collection

    async def create_new_document(self, document: dict) -> dict:
        """
        Create a new document in a collection.
        input: collection name, document
        return: created document
        """
        try:
            new_document = await self.collection.insert_one(document)
        except Exception as exception:
            logger.error("Error creating document %s error: %s",
                         document, exception)
            return None
        created_document = await self.collection.find_one({"_id": new_document.inserted_id})
        created_document["_id"] = str(created_document["_id"])
        return created_document
    
    async def set_index(self, index_list=[]):
        """
        Create index for a collection.
        input: collection name, index list
        """
        await self.collection.create_index(index_list, unique=True)

    async def get_number_of_documents(self, value_sort: str, sort_mode: int, limit: int = 1000) -> list:
        """
        Get n number of documents from a collection.
        input: collection name, n
        return: list of documents that Newest to Oldest
        """
        documents = await self.collection.find().sort(value_sort, sort_mode).to_list(limit)
        return documents

    async def get_document_by_query(self, query: dict) -> dict:
        """
        Get a document by query.
        input: collection name, query
        return: document
        """
        try:
            document = await self.collection.find_one(query)
        except Exception as exception:
            logger.error("Error getting document %s error: %s",
                         query, exception)
            return None
        return document

    async def get_documents_by_query(self, query: dict, length=1000) -> dict:
        """
        Get a document by query.
        input: collection name, query
        return: document
        """
        try:
            documents = await self.collection.find(query).to_list(length=length)
        except Exception as exception:
            logger.error("Error getting document %s error: %s",
                         query, exception)
            return None
        return documents

    async def get_document_by_query_and_projection(self,
                                                   query: dict,
                                                   projection: dict) -> dict:
        """
        Get a document by query.
        input: collection name, query
        return: document
        """
        try:
            document = await self.collection.find(query, projection)
        except Exception as exception:
            logger.error("Error getting document %s error: %s",
                         query, exception)
            return None
        return document

    async def get_document_by_id(self, document_id: str) -> dict:
        """
        Get a document by its id.
        input: collection name, document id
        return: document
        """
        try:
            document = await self.collection.find_one({"_id": ObjectId(document_id)})
        except Exception as exception:
            logger.error("Error getting ID %s error: %s",
                         document_id, exception)
            return None
        return document

    async def update_document_by_id(self, document_id: str, update_data: dict) -> dict:
        """
        Update a document by its id.
        input: collection name, document id
        return: document
        """
        try:
            document = await self.collection.find_one_and_update({"_id": ObjectId(document_id)},
                                                                 {"$set": update_data})
        except Exception as exception:
            logger.error("Error updating Agent ID %s error: %s",
                         document_id, exception)
            return None
        return document
    
    async def update_document_by_query(self, query: dict, update_data: dict) -> dict:
        """
        Update a document by its id.
        input: collection name, document id
        return: document
        """
        try:
            document = await self.collection.find_one_and_update(query,
                                                                 {"$set": update_data})
        except Exception as exception:
            logger.error("Error updating Agent ID %s error: %s",
                         query, exception)
            return None
        return document

    async def add_list_to_array_by_id(self, document_id: str, element: str, data: list) -> bool:
        """
        Add data to element array by ids.
        input: collection name, document id, element, data
        return: bool
        """
        try:
            await self.collection.find_one_and_update({"_id": ObjectId(document_id)},
                                {"$push": {element: {"$each": data}}}, 
                                projection={"_id": False})
        except Exception as exception:
            logger.error("Error updating ID %s error: %s",
                         document_id, exception)
            return None
        return True
    
    async def add_to_array_by_id(self, document_id: str, element: str, data: dict) -> dict:
        """
        Add data to element array by is.
        input: collection name, document id, element, data
        return: document
        """
        try:
            document = await self.collection.find_one_and_update({"_id": ObjectId(document_id)},
                                                                 {"$push": {element: data}})
        except Exception as exception:
            logger.error("Error updating Agent ID %s error: %s",
                         document_id, exception)
            return None
        return document

    async def remove_from_array_by_id(self, document_id: str, element: str, element_id: dict) -> dict:
        """
        Remove data from element array by id.
        """
        try:
            document = await self.collection.find_one_and_update({"_id": ObjectId(document_id)},
                                                                 {"$pull": {element: {"_id": ObjectId(element_id)}}})
        except Exception as exception:
            logger.error("Error updating Agent ID %s error: %s",
                         document_id, exception)
            return None
        return document
    
    async def remove_from_array_by_query(self, document_id: str, element: str, query: dict) -> dict:
        """
        Remove data from element array by query.
        """
        try:
            document = await self.collection.find_one_and_update({"_id": ObjectId(document_id)},
                                                                 {"$pull": {element: query}})
        except Exception as exception:
            logger.error("Error updating Agent ID %s error: %s",
                         document_id, exception)
            return None
        return document

    def close(self):
        self.client.close()