from tools.weaviate_tools.vectorizer import model
from config.weaviate_setup.weaviate_cloud_conn import create_connection_with_weaviate_cloud

def insert_data_to_activity_collection(data: dict):
    client = create_connection_with_weaviate_cloud()
    collection = client.collections.get("Activity")
    
    for doc in data:
        text = f"Activity: {doc['Activity']}. Description: {doc['Description']}. Type of Traveler: {doc['Type of Traveler']}. Budget: {doc['Budget details']}. Tips: {doc['Tips and Recommendations']}. Best for: {doc['For ']}. Category: {doc['CATEGORY']}."
        vector = model.encode(text).tolist()

        weaviate_data = {
            "Country": doc["Country"],
            "City": doc["City"],
            "Activity": doc["Activity"],
            "Description": doc["Description"],
            "TypeOfTraveler": doc["Type of Traveler"],
            "Duration": doc["Duration"],
            "BudgetInUSD": doc["Budget (USD)"],
            "BudgetDetails": doc["Budget details"],
            "TipsAndRecommendations": doc["Tips and Recommendations"],
            "For": doc["For "],
            "FamilyFriendly": doc["Family friendly"],
            "Category": doc["CATEGORY"],
        }

        uuid = collection.data.insert(properties=weaviate_data, vector=vector)

    client.close()