from tools.weaviate_tools.vectorizer import model
from config.weaviate_setup.weaviate_cloud_conn import create_connection_with_weaviate_cloud

def insert_data_to_transportation_collection(data: dict):
    client = create_connection_with_weaviate_cloud()
    collection = client.collections.get("Transportation")
    
    for doc in data:
        text = (f"Transport from {doc['From']} to {doc['To']} in {doc['Country']} via {doc['Transport Mode']}. "
                f"Provider: {doc['Provider']}. Schedule: {doc['Schedule']}. Route: {doc['Route Info']}. "
                f"Duration: {doc['Duration in hours']} hours. Price Range: {doc['Price Range in USD']} USD. "
                f"Cost Options: {doc['Cost Details and Options']}. Additional Info: {doc['Additional Info']}.")
        vector = model.encode(text).tolist()

        weaviate_data = {
            "Country": doc["Country"],
            "From": doc["From"],
            "To": doc["To"],
            "TransportMode": doc["Transport Mode"],
            "Provider": doc["Provider"],
            "Schedule": doc["Schedule"],
            "RouteInfo": doc["Route Info"],
            "DurationInHours": doc["Duration in hours"],
            "PriceRangeInUSD": doc["Price Range in USD"],
            "CostDetailsAndOptions": doc["Cost Details and Options"],
            "AdditionalInfo": doc["Additional Info"],
        }

        uuid = collection.data.insert(properties=weaviate_data, vector=vector)

    client.close()