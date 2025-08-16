from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables from a .env file (if present)
load_dotenv()

def create_connection_with_mongodb_cloud(connection_string):
    """Create a MongoClient using the provided connection string or the
    MONGODB_CLOUD_CONN environment variable.

    Args:
        connection_string: Optional MongoDB connection URI. If not provided,
            the function will read the MONGODB_CLOUD_CONN env var.

    Returns:
        MongoClient instance on success, or an error string on failure.
    """

    if not connection_string:
        connection_string = os.getenv("MONGODB_CLOUD_CONN")

    try:
        mongo_client = MongoClient(connection_string)
        return mongo_client
    except Exception as e:
        return f"there is an error while connecting with MongoDB Cloud: {e}"

