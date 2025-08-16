from config.mongodb_setup.mongodb_database_conn import create_connection_with_mongodb_database

def create_connection_with_mongodb_db_collection(database_name: str, collection_name: str):

    try:
        db = create_connection_with_mongodb_database(database_name)

        collection = db[collection_name]
        return collection
    except:
        return "there is an error while connecting with MongoDB Database Collection"