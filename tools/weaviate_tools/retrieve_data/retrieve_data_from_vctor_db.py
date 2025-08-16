from config.weaviate_setup.weaviate_cloud_conn import create_connection_with_weaviate_cloud
from tools.weaviate_tools.vectorizer import model

def retrieve_data(query: str, collection_name: str):

    client = create_connection_with_weaviate_cloud()
    collection = client.collections.get(collection_name)

    query_vector = model.encode(query).tolist()
    response = collection.query.near_vector(query_vector, limit=None)

    rag_res = [obj.properties for obj in response.objects]
    client.close()
    return rag_res
