from tools.weaviate_tools.vectorizer import model
from config.weaviate_setup.weaviate_cloud_conn import create_connection_with_weaviate_cloud

def insert_data_to_accommodations_collection(data: dict):
    client = create_connection_with_weaviate_cloud()
    collection = client.collections.get("Accommodations")
    
    for doc in data:
        text = (f"Accommodation: {doc['Accommodation Name']}. Type: {doc['Type']}. "
                f"Description: {doc['Accommodation Details']}. Price per night: {doc['Avg Night Price (USD)']} USD. "
                f"Location: {doc['City']}, {doc['Country']}.")
        vector = model.encode(text).tolist()

        weaviate_data = {
            "Country": doc["Country"],
            "City": doc["City"],
            "AccommodationName": doc["Accommodation Name"],
            "AccommodationDetails": doc["Accommodation Details"],
            "Type": doc["Type"],
            "AvgNightPriceInUSD": doc["Avg Night Price (USD)"],
        }

        uuid = collection.data.insert(properties=weaviate_data, vector=vector)
    
    client.close()
