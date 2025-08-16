from weaviate_cloud_conn import create_connection_with_weaviate_cloud
import weaviate.classes.config as wvc

client = create_connection_with_weaviate_cloud()

activity_collection = client.collections.create(
    name="Activity",
    properties=[
        wvc.Property(name="Country", data_type=wvc.DataType.TEXT),
        wvc.Property(name="City", data_type=wvc.DataType.TEXT),
        wvc.Property(name="Activity", data_type=wvc.DataType.TEXT),
        wvc.Property(name="Description", data_type=wvc.DataType.TEXT),
        wvc.Property(name="TypeOfTraveler", data_type=wvc.DataType.TEXT),
        wvc.Property(name="Duration", data_type=wvc.DataType.TEXT),
        wvc.Property(name="BudgetInUSD", data_type=wvc.DataType.TEXT),
        wvc.Property(name="BudgetDetails", data_type=wvc.DataType.TEXT),
        wvc.Property(name="TipsAndRecommendations", data_type=wvc.DataType.TEXT),
        wvc.Property(name="For", data_type=wvc.DataType.TEXT),
        wvc.Property(name="FamilyFriendly", data_type=wvc.DataType.TEXT),
        wvc.Property(name="Category", data_type=wvc.DataType.TEXT)
    ],
    vectorizer_config=wvc.Configure.Vectorizer.text2vec_huggingface(model="sentence-transformers/all-MiniLM-L6-v2"),
)

restaurants_collection = client.collections.create(
    name="Restaurants",
    properties=[
        wvc.Property(name="Country", data_type=wvc.DataType.TEXT),
        wvc.Property(name="City", data_type=wvc.DataType.TEXT),
        wvc.Property(name="RestaurantName", data_type=wvc.DataType.TEXT),
        wvc.Property(name="TypeOfCuisine", data_type=wvc.DataType.TEXT),
        wvc.Property(name="MealsServed", data_type=wvc.DataType.TEXT),
        wvc.Property(name="RecommendedDish", data_type=wvc.DataType.TEXT),
        wvc.Property(name="MealDescription", data_type=wvc.DataType.TEXT),
        wvc.Property(name="AvgPricePerPersonInUSD", data_type=wvc.DataType.TEXT),
        wvc.Property(name="BudgetRange", data_type=wvc.DataType.TEXT),
        wvc.Property(name="Suitability", data_type=wvc.DataType.TEXT)
    ],
    vectorizer_config=wvc.Configure.Vectorizer.text2vec_huggingface(model="sentence-transformers/all-MiniLM-L6-v2"),
)

dishes_collection = client.collections.create(
    name="Dishes",
    properties=[
        wvc.Property(name="Country", data_type=wvc.DataType.TEXT),
        wvc.Property(name="City", data_type=wvc.DataType.TEXT),
        wvc.Property(name="DishName", data_type=wvc.DataType.TEXT),
        wvc.Property(name="DishDetails", data_type=wvc.DataType.TEXT),
        wvc.Property(name="Type", data_type=wvc.DataType.TEXT),
        wvc.Property(name="AvgPriceInUSD", data_type=wvc.DataType.TEXT),
        wvc.Property(name="BestFor", data_type=wvc.DataType.TEXT)
    ],
    vectorizer_config=wvc.Configure.Vectorizer.text2vec_huggingface(model="sentence-transformers/all-MiniLM-L6-v2"),
)

accommodations_collection = client.collections.create(
    name="Accommodations",
    properties=[
        wvc.Property(name="Country", data_type=wvc.DataType.TEXT),
        wvc.Property(name="City", data_type=wvc.DataType.TEXT),
        wvc.Property(name="AccommodationName", data_type=wvc.DataType.TEXT),
        wvc.Property(name="AccommodationDetails", data_type=wvc.DataType.TEXT),
        wvc.Property(name="Type", data_type=wvc.DataType.TEXT),
        wvc.Property(name="AvgNightPriceInUSD", data_type=wvc.DataType.TEXT)
    ],
    vectorizer_config=wvc.Configure.Vectorizer.text2vec_huggingface(model="sentence-transformers/all-MiniLM-L6-v2"),
)

transportation_collection = client.collections.create(
    name="Transportation",
    properties=[
        wvc.Property(name="Country", data_type=wvc.DataType.TEXT),
        wvc.Property(name="From", data_type=wvc.DataType.TEXT),
        wvc.Property(name="To", data_type=wvc.DataType.TEXT),
        wvc.Property(name="TransportMode", data_type=wvc.DataType.TEXT),
        wvc.Property(name="Provider", data_type=wvc.DataType.TEXT),
        wvc.Property(name="Schedule", data_type=wvc.DataType.TEXT),
        wvc.Property(name="RouteInfo", data_type=wvc.DataType.TEXT),
        wvc.Property(name="DurationInHours", data_type=wvc.DataType.TEXT),
        wvc.Property(name="PriceRangeInUSD", data_type=wvc.DataType.TEXT),
        wvc.Property(name="CostDetailsAndOptions", data_type=wvc.DataType.TEXT),
        wvc.Property(name="AdditionalInfo", data_type=wvc.DataType.TEXT)
    ],
    vectorizer_config=wvc.Configure.Vectorizer.text2vec_huggingface(model="sentence-transformers/all-MiniLM-L6-v2"),
)

visa_collection = client.collections.create(
    name="Visa",
    properties=[
        wvc.Property(name="Country", data_type=wvc.DataType.TEXT),
        wvc.Property(name="Question", data_type=wvc.DataType.TEXT),
        wvc.Property(name="Answer", data_type=wvc.DataType.TEXT)
    ],
    vectorizer_config=wvc.Configure.Vectorizer.text2vec_huggingface(model="sentence-transformers/all-MiniLM-L6-v2"),
)

seasonal_collection = client.collections.create(
    name="Seasonal",
    properties=[
        wvc.Property(name="Country", data_type=wvc.DataType.TEXT),
        wvc.Property(name="Question", data_type=wvc.DataType.TEXT),
        wvc.Property(name="Answer", data_type=wvc.DataType.TEXT)
    ],
    vectorizer_config=wvc.Configure.Vectorizer.text2vec_huggingface(model="sentence-transformers/all-MiniLM-L6-v2"),
)

scams_collection = client.collections.create(
    name="Scams",
    properties=[
        wvc.Property(name="Country", data_type=wvc.DataType.TEXT),
        wvc.Property(name="City", data_type=wvc.DataType.TEXT),
        wvc.Property(name="ScamType", data_type=wvc.DataType.TEXT),
        wvc.Property(name="Description", data_type=wvc.DataType.TEXT),
        wvc.Property(name="Location", data_type=wvc.DataType.TEXT),
        wvc.Property(name="PreventionTips", data_type=wvc.DataType.TEXT)
    ],
    vectorizer_config=wvc.Configure.Vectorizer.text2vec_huggingface(model="sentence-transformers/all-MiniLM-L6-v2"),
)

client.close()