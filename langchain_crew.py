import json
import os
from typing import List, Union
from pydantic import BaseModel, Field
from langchain_ollama.llms import OllamaLLM
from langchain.agents import Tool, create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate
from config.weaviate_setup.weaviate_cloud_conn import create_connection_with_weaviate_cloud
from tools.weaviate_tools.vectorizer import model

# Custom Weaviate search tool
def weaviate_search(query: str) -> str:
    """Search the Weaviate vector database for travel activities or restaurants based on the query."""
    client = create_connection_with_weaviate_cloud()

    if "restaurant" in query.lower():
        collection = client.collections.get("Restaurants")
        return_properties = [
            "country", "city", "restaurant_name", "type_of_cuisine", "meals_served",
            "recommended_dish", "meal_description", "avg_price_per_person",
            "budget_range", "suitability"
        ]
        key = "restaurants"
    else:
        collection = client.collections.get("Activity")
        return_properties = [
            "country", "city", "activity", "description", "typeOfTraveler", "duration",
            "budgetInUSD", "budgetDetails", "tipsAndRecommendations", "for", "familyFriendly", "category"
        ]
        key = "activities"

    query_vector = model.encode(query).tolist()
    response = collection.query.near_vector(
        query_vector,
        certainty=0.65,
        limit=10,
        return_properties=return_properties
    )

    results = [obj.properties for obj in response.objects]
    client.close()
    return json.dumps({key: results})

weaviate_tool = Tool(
    name="WeaviateSearch",
    func=weaviate_search,
    description="Search the Weaviate vector database for travel activities or restaurants based on the query."
)

# Output schemas
class SingleActivitySchema(BaseModel):
    country: str
    city: str
    activity: str
    description: str
    typeOfTraveler: str
    duration: str
    budgetInUSD: str
    budgetDetails: str
    tipsAndRecommendations: str
    for_: str = Field(..., alias="for")
    familyFriendly: str
    category: str

class SingleRestaurantSchema(BaseModel):
    country: str
    city: str
    restaurant_name: str
    type_of_cuisine: str
    meals_served: str
    recommended_dish: str
    meal_description: str
    avg_price_per_person: float
    budget_range: str
    suitability: str

class OutputSchema(BaseModel):
    activities: Union[List[SingleActivitySchema], None] = None
    restaurants: Union[List[SingleRestaurantSchema], None] = None

# Prompt template
react_prompt = PromptTemplate.from_template(
    """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer

Thought: you should always think about what to do

Action: the action to take, should be one of [{tool_names}]

Action Input: the input to the action

Observation: the result of the action

... (this Thought/Action/Action Input/Observation can repeat N times)

Thought: I now know the final answer

Final Answer: the final answer to the original input question, formatted as a JSON array of either activities or restaurants. After receiving the list, review them to ensure they are relevant to the original query. If any item does not seem related, exclude it from the final output.

Begin!

Question: {input}

Thought: {agent_scratchpad}"""
)

llm = OllamaLLM(model="llama3.1:8b-instruct-q8_0", base_url="http://localhost:11434")
agent = create_react_agent(llm, [weaviate_tool], react_prompt)
executor = AgentExecutor(agent=agent, tools=[weaviate_tool], verbose=True)

def run_agent(query: str, output_file: str = "result.json") -> str:
    result = executor.invoke({"input": query})
    print(f"Raw agent output: {result}")

    agent_output = result.get("output", str(result))
    final_answer_start = agent_output.find("Final Answer:")

    if final_answer_start != -1:
        final_answer = agent_output[final_answer_start + len("Final Answer:"):].strip()
        try:
            data = json.loads(final_answer)
            if "activities" in data:
                output = OutputSchema(activities=[SingleActivitySchema(**a) for a in data["activities"]])
            elif "restaurants" in data:
                output = OutputSchema(restaurants=[SingleRestaurantSchema(**r) for r in data["restaurants"]])
            else:
                return "Error: Unexpected schema in agent output."

            with open(output_file, "w") as f:
                json.dump(output.dict(by_alias=True), f, indent=2)
            return final_answer
        except json.JSONDecodeError:
            return "Error: Could not parse the agent's output as JSON: " + final_answer
    return "Error: No Final Answer found in the agent's output: " + agent_output

if __name__ == "__main__":
    query = "What are the top family-friendly restaurants in Cairo?"
    result = run_agent(query, output_file=os.path.join("/", "result.json"))
    print("Result:", result)
