from pymongo import MongoClient

def create_connection_with_mongodb_cloud(connection_string: str = "mongodb+srv://ah8081189:21-12-2004@cluster0.xosvf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"):

    try:
        mongo_client = MongoClient(connection_string)
        return mongo_client
    except:
        return "there is an error while connecting with MongoDB Cloud"
    
