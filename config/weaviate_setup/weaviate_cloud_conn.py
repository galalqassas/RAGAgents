import weaviate
from weaviate.classes.init import Auth

def create_connection_with_weaviate_cloud(cluster_url: str = "https://tnvaqaphruqmynobaagzvq.c0.us-west3.gcp.weaviate.cloud",
                                          auth_credentials: str = "3kYEomCKTWha7sSjI8dkT5CJPdKE2ivfySMa"):

    try:
        client = weaviate.connect_to_weaviate_cloud(
            cluster_url=cluster_url,
            auth_credentials=Auth.api_key(auth_credentials)
        )
        return client
    except:
        return "there is an error while connecting with Weaviate Cloud"