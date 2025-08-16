from tools.weaviate_tools.vectorizer import model
from config.weaviate_setup.weaviate_cloud_conn import create_connection_with_weaviate_cloud

def insert_data_to_dishes_collection(data: dict):
    client = create_connection_with_weaviate_cloud()
    collection = client.collections.get("Dishes")
    
    for doc in data:
        text = (f"Dish: {doc['Dish Name']}. Description: {doc['Dish Details']}. "
                f"Type: {doc['Type']}. Price: {doc['Avg Price (USD)']} USD. "
                f"Best For: {doc['Best For']}. Location: {doc['City']}, {doc['Country']}.")
        vector = model.encode(text).tolist()

        weaviate_data = {
            "Country": doc["Country"],
            "City": doc["City"],
            "DishName": doc["Dish Name"],
            "DishDetails": doc["Dish Details"],
            "Type": doc["Type"],
            "AvgPriceInUSD": str(doc["Avg Price (USD)"]),
            "BestFor": doc["Best For"],
        }

        uuid = collection.data.insert(properties=weaviate_data, vector=vector)

    client.close()