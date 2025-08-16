from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, Optional
import json
from config.weaviate_setup.weaviate_cloud_conn import create_connection_with_weaviate_cloud
from tools.weaviate_tools.vectorizer import model


class WeaviateToolSchema(BaseModel):
    query: str = Field(..., description="The query to search and retrieve relevant information.")
    intent: str = Field(..., description="The classified agent type such as 'activity', 'dish', etc.")


class WeaviateTool(BaseTool):
    name: str = "WeaviateTool"
    description: str = "Search Weaviate for activities, dishes, restaurants, visa info, etc."
    args_schema: Type[BaseModel] = WeaviateToolSchema

    def _run(self, query: str, intent: str) -> str:
        client = create_connection_with_weaviate_cloud()
        print(f"Weaviate Query: {query}")
        print(f"Intent: {intent}")

        collection_map = {
            "activity": {
                "name": "Activity",
                "properties": ["Country", "City", "Activity", "Description", "TypeOfTraveler", "Duration", "BudgetInUSD", "BudgetDetails", "TipsAndRecommendations", "For", "FamilyFriendly", "Category"]
            },
            "dish": {
                "name": "Dishes",
                "properties": ["Country", "City", "DishName", "DishDetails", "Type", "AvgPriceInUSD", "BestFor"]
            },
            "restaurant": {
                "name": "Restaurants",
                "properties": ["Country", "City", "RestaurantName", "TypeOfCuisine", "MealsServed", "RecommendedDish", "MealDescription", "AvgPricePerPersonInUSD", "BudgetRange", "Suitability"]
            },
            "scam": {
                "name": "Scams",
                "properties": ["Country", "City", "ScamType", "Description", "Location", "PreventionTips"]
            },
            "accommodation": {
                "name": "Accommodations",
                "properties": ["Country", "City", "AccommodationName", "AccommodationDetails", "Type", "AvgNightPriceInUSD"]
            },
            "transportation": {
                "name": "Transportation",
                "properties": ["Country", "From", "To", "TransportMode", "Provider", "Schedule", "RouteInfo", "DurationInHours", "PriceRangeInUSD", "CostDetailsAndOptions", "AdditionalInfo"]
            },
            "visa": {
                "name": "Visa",
                "properties": ["Country", "Question", "Answer"]
            },
            "seasonal": {
                "name": "Seasonal",
                "properties": ["Country", "Question", "Answer"]
            }
        }

        intent = intent.lower().strip()
        if intent not in collection_map:
            return json.dumps({"error": f"Unknown intent '{intent}' — no matching collection."})

        collection_name = collection_map[intent]["name"]
        return_properties = collection_map[intent]["properties"]

        try:
            collection = client.collections.get(collection_name)
            query_vector = model.encode(query).tolist()
            response = collection.query.near_vector(
                query_vector,
                certainty=0.65,
                limit=15,
                return_properties=return_properties
            )
            rag_res = [obj.properties for obj in response.objects]
            client.close()
            return json.dumps({collection_name.lower(): rag_res})
        except Exception as e:
            client.close()
            return json.dumps({"error": str(e)})
