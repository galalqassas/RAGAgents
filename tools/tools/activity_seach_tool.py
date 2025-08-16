from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, Optional
import json
from config.weaviate_setup.weaviate_cloud_conn import create_connection_with_weaviate_cloud
from tools.weaviate_tools.vectorizer import model

class WeaviateToolSchema(BaseModel):
    query: str = Field(..., description="The query to search and retrieve relevant information from the Weaviate database.")

class WeaviateTool(BaseTool):
    name: str = "WeaviateTool"
    description: str = "Search the Weaviate database for activities, dishes, restaurants, accommodations, or scams."
    args_schema: Type[BaseModel] = WeaviateToolSchema
    query: Optional[str] = None

    def _run(self, query: str) -> str:
        client = create_connection_with_weaviate_cloud()
        print(f"Weaviate Query: {query}")

        if "activity" in query.lower():
            collection_name = "Activity"
            return_properties = ["Country", "City", "Activity", "Description", "TypeOfTraveler", "Duration", "BudgetInUSD", "BudgetDetails", "TipsAndRecommendations", "For", "FamilyFriendly", "Category"]
        elif "dish" in query.lower():
            collection_name = "Dishes"
            return_properties = ["Country", "City", "DishName", "DishDetails", "Type", "AvgPriceInUSD", "BestFor"]
        elif "restaurant" in query.lower() or "dining" in query.lower():
            collection_name = "Restaurants"
            return_properties = ["Country", "City", "RestaurantName", "TypeOfCuisine", "MealsServed", "RecommendedDish", "MealDescription", "AvgPricePerPersonInUSD", "BudgetRange", "Suitability"]
        elif "scam" in query.lower() or "fraud" in query.lower() or "safety" in query.lower() or "tourist trap" in query.lower():
            collection_name = "Scams"
            return_properties = ["Country", "City", "ScamType", "Description", "Location", "PreventionTips"]
        elif any(term in query.lower() for term in ["accommodation", "hotel", "motel", "hostel"]):
            collection_name = "Accommodations"
            return_properties = ["Country", "City", "AccommodationName", "AccommodationDetails", "Type", "AvgNightPriceInUSD"]
        elif "transportation" in query.lower():
            collection_name = "Transportation"
            return_properties = ["Country", "From", "To", "TransportMode", "Provider", "Schedule", "RouteInfo", "DurationInHours", "PriceRangeInUSD", "CostDetailsAndOptions", "AdditionalInfo"]
        elif "visa" in query.lower():
            collection_name = "Visa"
            return_properties = ["Country", "Question", "Answer"]
        elif "seasonal" in query.lower():
            collection_name = "Seasonal"
            return_properties = ["Country", "Question", "Answer"]
        else:
            return json.dumps({"error": "Query did not match any known collections."})

        try:
            collection = client.collections.get(collection_name)
            query_vector = model.encode(query).tolist()
            response = collection.query.near_vector(query_vector, certainty=0.65, limit=15, return_properties=return_properties)
            rag_res = [obj.properties for obj in response.objects]
            client.close()
            return json.dumps({collection_name.lower(): rag_res})
        except Exception as e:
            client.close()
            return json.dumps({"error": str(e)})
