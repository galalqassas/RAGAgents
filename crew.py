import os
import json
from typing import List, Dict, Optional, Any
import numpy as np
from pydantic import BaseModel, Field
from crewai import Agent, Crew, Process, Task, LLM
from tools.activity_seach_tool import WeaviateTool
from tools.weaviate_tools.vectorizer import model as embedding_model
from tools.classifier import classify_query_intent
import google.generativeai as genai
from dotenv import load_dotenv

# Output schemas
class SingleAccommodationSchema(BaseModel):
    Country: str = Field(...)
    City: str = Field(...)
    AccommodationName: str = Field(...)
    AccommodationDetails: str = Field(...)
    Type: str = Field(...)
    AvgNightPriceInUSD: str = Field(...)

class AccommodationOutputSchema(BaseModel):
    accommodations: List[SingleAccommodationSchema]

class SingleDishSchema(BaseModel):
    Country: str = Field(...)
    City: str = Field(...)
    DishName: str = Field(...)
    DishDetails: str = Field(...)
    Type: str = Field(...)
    AvgPriceInUSD: str = Field(...)
    BestFor: str = Field(...)

class DishOutputSchema(BaseModel):
    dishes: List[SingleDishSchema]

class SingleActivitySchema(BaseModel):
    Country: str = Field(...)
    City: str = Field(...)
    Activity: str = Field(...)
    Description: str = Field(...)
    TypeOfTraveler: str = Field(...)
    Duration: str = Field(...)
    BudgetInUSD: str = Field(...)
    BudgetDetails: str = Field(...)
    TipsAndRecommendations: str = Field(...)
    For: str = Field(...)
    FamilyFriendly: str = Field(...)
    Category: str = Field(...)

class ActivityOutputSchema(BaseModel):
    activities: List[SingleActivitySchema]

class SingleRestaurantSchema(BaseModel):
    Country: str = Field(...)
    City: str = Field(...)
    RestaurantName: str = Field(...)
    TypeOfCuisine: str = Field(...)
    MealsServed: str = Field(...)
    RecommendedDish: str = Field(...)
    MealDescription: str = Field(...)
    AvgPricePerPersonInUSD: str = Field(...)
    BudgetRange: str = Field(...)
    Suitability: str = Field(...)

class RestaurantOutputSchema(BaseModel):
    restaurants: List[SingleRestaurantSchema]

class SingleScamSchema(BaseModel):
    Country: str = Field(...)
    City: str = Field(...)
    ScamType: str = Field(...)
    Description: str = Field(...)
    Location: str = Field(...)
    PreventionTips: str = Field(...)

class ScamOutputSchema(BaseModel):
    scams: List[SingleScamSchema]

class SingleTransportationSchema(BaseModel):
    Country: str = Field(...)
    From: str = Field(...)
    To: str = Field(...)
    TransportMode: str = Field(...)
    Provider: str = Field(...)
    Schedule: str = Field(...)
    RouteInfo: str = Field(...)
    DurationInHours: str = Field(...)
    PriceRangeInUSD: str = Field(...)
    CostDetailsAndOptions: str = Field(...)
    AdditionalInfo: str = Field(...)

class TransportationOutputSchema(BaseModel):
    transportations: List[SingleTransportationSchema]

class SingleVisaSchema(BaseModel):
    Country: str = Field(...)
    Question: str = Field(...)
    Answer: str = Field(...)

class VisaOutputSchema(BaseModel):
    visas: List[SingleVisaSchema]

class SingleSeasonalSchema(BaseModel):
    Country: str = Field(...)
    Question: str = Field(...)
    Answer: str = Field(...)

class SeasonalOutputSchema(BaseModel):
    seasonals: List[SingleSeasonalSchema]

class AgenticRagCrew:
    def __init__(self):
        # Load environment and set up Gemini API for filter extraction
        load_dotenv()
        gemini_key = os.getenv('GEMINI_API_KEY')
        genai.configure(api_key=gemini_key)

        self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Initialize LLM for agents
        self.llm = LLM(model="ollama/llama3.1:8b-instruct-q8_0", base_url="http://localhost:11434")
        
        # Create agents and tasks
        self._create_agents_and_tasks()

    def _create_agents_and_tasks(self):
        """Create all agents and their associated tasks"""
        # Define agent configurations
        agent_configs = {
            "accommodation": {
                "role": "Accommodation Retrieval Agent",
                "goal": "Retrieve accommodations from the database",
                "backstory": "Find information about accommodation names, details, types, and average night prices (USD)",
                "output_schema": AccommodationOutputSchema,
                "output_file": "accommodation_result.json"
            },
            "restaurant": {
                "role": "Restaurant Retrieval Agent",
                "goal": "Retrieve restaurants from the database",
                "backstory": "Find restaurants based on query from the Weaviate DB",
                "output_schema": RestaurantOutputSchema,
                "output_file": "restaurant_result.json"
            },
            "visa": {
                "role": "Visa Information Retrieval Agent",
                "goal": "Retrieve visa and travel timing information from the database",
                "backstory": "Find information about visa requirements and regulations for destinations",
                "output_schema": VisaOutputSchema,
                "output_file": "visa_result.json"
            },
            "seasonal": {
                "role": "Seasonal Information Retrieval Agent",
                "goal": "Retrieve seasonal travel information from the database",
                "backstory": "Find information about best times to visit, peak seasons, and weather patterns",
                "output_schema": SeasonalOutputSchema,
                "output_file": "seasonal_result.json"
            },
            "dish": {
                "role": "Dish Retrieval Agent",
                "goal": "Retrieve local dishes from the database",
                "backstory": "Find popular local dishes, their details, types, and pricing",
                "output_schema": DishOutputSchema,
                "output_file": "dish_result.json"
            },
            "transportation": {
                "role": "Transportation Retrieval Agent",
                "goal": "Retrieve transportation options from the database",
                "backstory": "Find routes, providers, schedules, and prices for transportation",
                "output_schema": TransportationOutputSchema,
                "output_file": "transportation_result.json"
            },
            "activity": {
                "role": "Senior RAG Retrieval Agent",
                "goal": "Answer questions about activities in the Weaviate database",
                "backstory": "Find travel activities from Weaviate DB",
                "output_schema": ActivityOutputSchema,
                "output_file": "activity_result.json"
            }
        }
        
        # Create agents and tasks
        self.agents = {}
        self.tasks = {}
        
        for agent_type, config in agent_configs.items():
            # Create agent
            self.agents[agent_type] = Agent(
                role=config["role"],
                goal=config["goal"],
                backstory=config["backstory"],
                tools=[WeaviateTool()],
                verbose=True,
                llm=self.llm
            )
            
            # Create task
            self.tasks[agent_type] = Task(
                description=f"Retrieve {agent_type} data related to {{query}}. Use WeaviateTool and ensure results are specific and structured.",
                expected_output=f"Relevant {agent_type} data as JSON",
                output_json=config["output_schema"],
                output_file=os.path.join("/", config["output_file"]),
                agent=self.agents[agent_type]
            )
        
        # Create main crew with all agents and tasks
        self.crew = Crew(
            agents=list(self.agents.values()),
            tasks=list(self.tasks.values()),
            process=Process.sequential,
            verbose=True,
            llm=self.llm
        )

    def extract_filters_from_query(self, query: str) -> Dict[str, str]:
        """Extract filters from a query using Gemini API"""
        prompt = (
            "Analyze the following query and extract filters for budget, dietary preferences, city, type, duration, and suitability. "
            "Return your answer as a JSON object with these keys: 'budget', 'dietary', 'city', 'type', 'duration', 'suitability'. "
            "If no filter is present, set the value to an empty string ('').\n\n"
            f"Query: {query}"
        )
        
        response = self.gemini_model.generate_content(prompt)
        try:
            filters = json.loads(response.text)
            return {k: v for k, v in filters.items() if v}  # Remove empty values
        except (json.JSONDecodeError, ValueError) as e:
            print(f"[Warning] Failed to parse filters from query: {e}")
            return {}

    def run_task_by_classified_intent(self, query: str, filters: Dict[str, str] = None):
        """Run tasks based on classified intents with ranking and filtering"""
        # Get filters if not provided
        if filters is None:
            filters = self.extract_filters_from_query(query)
        print(f"[Extracted Filters]: {filters}")
        
        # Classify intent
        intent_result = classify_query_intent(query)
        print(f"[Classified Intent]: {intent_result}")
        
        # Convert to list of intents
        intents = [intent_result.lower()] if isinstance(intent_result, str) else [i.lower() for i in intent_result]
        
        # Map intent to task
        results = {}
        
        for intent in intents:
            task = self.tasks.get(intent)
            if not task:
                print(f"[Warning] Unknown intent: {intent}")
                continue
            
            # Run task with temporary crew
            temp_crew = Crew(
                agents=[task.agent],
                tasks=[task],
                verbose=True,
                llm=self.llm,
                process=Process.sequential
            )
            
            output = temp_crew.kickoff(inputs={"query": query, "intent": intent})
            raw_result = output.json_dict if hasattr(output, 'json_dict') else str(output)
            
            # Process results
            if isinstance(raw_result, dict):
                ranked_filtered_result = self._rank_and_filter_results(raw_result, query, filters, intent)
                results[task.agent.role] = ranked_filtered_result
            else:
                results[task.agent.role] = raw_result
        
        if not results:
            raise ValueError(f"No supported intents found in: {intents}")
        
        # Save results
        output_file = "crew_result.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=4)
        print(f"[Result saved to]: {output_file}")
        
        return results

    def _rank_and_filter_results(self, result: Dict, query: str, filters: Dict[str, str], intent: str) -> Dict:
        """Rank and filter results based on query and filters"""
        # Define field mappings for different intents
        field_mappings = {
            "restaurant": {
                "items_key": "restaurants",
                "key_field": "RestaurantName",
                "desc_field": "MealDescription",
                "price_field": "AvgPricePerPersonInUSD",
                "type_field": "TypeOfCuisine",
                "suitability_field": "Suitability",
                "duration_field": None
            },
            "dish": {
                "items_key": "dishes",
                "key_field": "DishName",
                "desc_field": "DishDetails",
                "price_field": "AvgPriceInUSD",
                "type_field": "Type",
                "suitability_field": "BestFor",
                "duration_field": None
            },
            "transportation": {
                "items_key": "transportations",
                "key_field": "TransportMode",
                "desc_field": "RouteInfo",
                "price_field": "PriceRangeInUSD",
                "type_field": "TransportMode",
                "suitability_field": None,
                "duration_field": "DurationInHours"
            },
            "activity": {
                "items_key": "activities",
                "key_field": "Activity",
                "desc_field": "Description",
                "price_field": "BudgetInUSD",
                "type_field": "Category",
                "suitability_field": "For",
                "duration_field": "Duration"
            },
            "accommodation": {
                "items_key": "accommodations",
                "key_field": "AccommodationName",
                "desc_field": "AccommodationDetails",
                "price_field": "AvgNightPriceInUSD",
                "type_field": "Type",
                "suitability_field": None,
                "duration_field": None
            },
            "visa": {
                "items_key": "visas",
                "key_field": "Question",
                "desc_field": "Answer",
                "price_field": None,
                "type_field": None,
                "suitability_field": None,
                "duration_field": None
            },
            "seasonal": {
                "items_key": "seasonals",
                "key_field": "Question",
                "desc_field": "Answer",
                "price_field": None,
                "type_field": None,
                "suitability_field": None,
                "duration_field": None
            }
        }
        
        # Get field mapping for current intent
        mapping = field_mappings.get(intent)
        if not mapping or mapping["items_key"] not in result:
            return result
        
        items = result[mapping["items_key"]]
        key_field = mapping["key_field"]
        desc_field = mapping["desc_field"]
        price_field = mapping["price_field"]
        type_field = mapping["type_field"]
        suitability_field = mapping["suitability_field"]
        duration_field = mapping["duration_field"]
        
        # 1. Rank by similarity
        query_embedding = embedding_model.encode(query.lower())
        
        def calculate_similarity(item):
            item_text = f"{item.get(key_field, '')} {item.get(desc_field, '')}".lower()
            item_embedding = embedding_model.encode(item_text)
            similarity = np.dot(query_embedding, item_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(item_embedding)
            )
            return similarity if not np.isnan(similarity) else 0.0
        
        ranked_items = sorted(items, key=calculate_similarity, reverse=True)
        filtered_items = ranked_items
        
        # 2. Apply filters
        # City filter
        if "city" in filters:
            city_filter = filters["city"].lower()
            filtered_items = [item for item in filtered_items if item.get("City", "").lower() == city_filter]
        
        # Budget filter
        if "budget" in filters and price_field:
            budget_value = filters["budget"].lower()
            try:
                # Calculate price statistics
                prices = []
                for item in items:
                    if item.get(price_field):
                        # Handle various price formats
                        price_str = str(item.get(price_field)).replace('$', '').replace('~', '')
                        try:
                            if '-' in price_str:  # Handle ranges
                                price_str = price_str.split('-')[0]
                            prices.append(float(price_str))
                        except ValueError:
                            continue
                
                if prices:
                    price_mean = np.mean(prices)
                    price_std = np.std(prices) or 1.0
                    
                    # Apply budget filter
                    if budget_value in ["low", "cheap", "affordable"]:
                        threshold = price_mean - price_std
                        filtered_items = [
                            item for item in filtered_items 
                            if self._extract_price(item.get(price_field, float('inf'))) <= threshold
                        ]
                    elif budget_value in ["medium", "moderate"]:
                        threshold_low = price_mean - price_std
                        threshold_high = price_mean + price_std
                        filtered_items = [
                            item for item in filtered_items
                            if threshold_low <= self._extract_price(item.get(price_field, float('inf'))) <= threshold_high
                        ]
                    elif budget_value in ["high", "expensive", "luxury"]:
                        threshold = price_mean + price_std
                        filtered_items = [
                            item for item in filtered_items 
                            if self._extract_price(item.get(price_field, float('inf'))) >= threshold
                        ]
            except Exception as e:
                print(f"[Warning] Error in budget filtering: {e}")
        
        # Apply remaining filters if needed (simplified implementation)
        for filter_name, field in [
            ("type", type_field),
            ("suitability", suitability_field)
        ]:
            if filter_name in filters and field:
                filter_embedding = embedding_model.encode(filters[filter_name].lower())
                
                # Sort by similarity to filter
                def get_field_similarity(item):
                    field_text = str(item.get(field, "")).lower()
                    field_embedding = embedding_model.encode(field_text)
                    sim = np.dot(filter_embedding, field_embedding) / (
                        np.linalg.norm(filter_embedding) * np.linalg.norm(field_embedding)
                    )
                    return sim if not np.isnan(sim) else 0.0
                
                filtered_items = sorted(filtered_items, key=get_field_similarity, reverse=True)
        
        return {mapping["items_key"]: filtered_items}
    
    def _extract_price(self, price_value):
        """Extract numeric price from various formats"""
        if isinstance(price_value, (int, float)):
            return float(price_value)
        
        price_str = str(price_value).replace('$', '').replace('~', '')
        try:
            if '-' in price_str:  # Handle ranges
                price_str = price_str.split('-')[0]
            return float(price_str)
        except ValueError:
            return float('inf')  # Default to infinity if can't parse
