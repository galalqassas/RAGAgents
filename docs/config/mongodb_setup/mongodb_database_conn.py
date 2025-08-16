from config.mongodb_setup.mongodb_cloud_conn import create_connection_with_mongodb_cloud

def create_connection_with_mongodb_database(database_name: str):

    try:
        mongo_client = create_connection_with_mongodb_cloud()

        db = mongo_client[database_name]
        return db
    except:
        return "there is an error while connecting with MongoDB Database"