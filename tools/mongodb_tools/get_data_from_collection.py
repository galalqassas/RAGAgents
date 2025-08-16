from config.mongodb_setup.mongodb_collection_conn import create_connection_with_mongodb_db_collection

def get_data_from_mongodb_collection(database_name: str, collection_name: str):

    try:
        collection = create_connection_with_mongodb_db_collection(database_name=database_name, 
                                                                  collection_name=collection_name)
        
        documents = list(collection.find({}, {"_id": 0}))
        return documents
    except:
        return f"Error while fetching data from mongodb collection: {collection_name}"
