from tools.weaviate_tools.vectorizer import model
from config.weaviate_setup.weaviate_cloud_conn import create_connection_with_weaviate_cloud

def insert_data_to_seasonal_collection(data: dict):
    client = create_connection_with_weaviate_cloud()
    collection = client.collections.get("Scams")
    
    for doc in data:
        text = (f"Country: {doc['Country']}. City: {doc['City']}. "
                f"Scam Type: {doc['Scam Type']}. Description: {doc['Description']}. "
                f"Location: {doc['Location']}. Prevention Tips: {doc['Prevention Tips']}.")
        vector = model.encode(text).tolist()

        weaviate_data = {
            "Country": doc["Country"],
            "City": doc["City"],
            "ScamType": doc["Scam Type"],
            "Description": doc["Description"],
            "Location": doc["Location"],
            "PreventionTips": doc["Prevention Tips"],
        }

        uuid = collection.data.insert(properties=weaviate_data, vector=vector)

    client.close()