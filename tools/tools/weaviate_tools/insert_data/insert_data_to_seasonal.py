from tools.weaviate_tools.vectorizer import model
from config.weaviate_setup.weaviate_cloud_conn import create_connection_with_weaviate_cloud

def insert_data_to_seasonal_collection(data: dict):
    client = create_connection_with_weaviate_cloud()
    collection = client.collections.get("Seasonal")
    
    for doc in data:
        text = (f"Country: {doc['Country']}. Question: {doc['Question']}. Answer: {doc['Answer']}.")
        vector = model.encode(text).tolist()

        weaviate_data = {
            "Country": doc["Country"],
            "Question": doc["Question"],
            "Answer": doc["Answer"],
        }

        uuid = collection.data.insert(properties=weaviate_data, vector=vector)

    client.close()