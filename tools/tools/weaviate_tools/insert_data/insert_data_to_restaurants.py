from tools.weaviate_tools.vectorizer import model
from config.weaviate_setup.weaviate_cloud_conn import create_connection_with_weaviate_cloud

def insert_data_to_restaurants_collection(data: dict):
    client = create_connection_with_weaviate_cloud()
    collection = client.collections.get("Restaurants")
    
    for doc in data:
        text = (f"Restaurant: {doc['Restaurant Name']}. Cuisine: {doc['Type of Cuisine']}. "
                f"Meals Served: {doc['Meals Served']}. Recommended Dish: {doc['Recommended Dish']}. "
                f"Description: {doc['Meal Description']}. Price: {doc['Avg Price per Person (USD)']} USD. "
                f"Budget Range: {doc['Budget Range']}. Suitability: {doc['Suitability']}. "
                f"Location: {doc['City']}, {doc['Country']}.")
        
        vector = model.encode(text).tolist()

        weaviate_data = {
            "Country": doc["Country"],
            "City": doc["City"],
            "RestaurantName": doc["Restaurant Name"],
            "TypeOfCuisine": doc["Type of Cuisine"],
            "MealsServed": doc["Meals Served"],
            "RecommendedDish": doc["Recommended Dish"],
            "MealDescription": doc["Meal Description"],
            "AvgPricePerPersonInUSD": str(doc["Avg Price per Person (USD)"]),
            "BudgetRange": doc["Budget Range"],
            "Suitability": doc["Suitability"],
        }

        uuid = collection.data.insert(properties=weaviate_data, vector=vector)

    client.close()