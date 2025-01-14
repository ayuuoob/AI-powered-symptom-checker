from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from qdrant_client.http.exceptions import UnexpectedResponse
from dotenv import load_dotenv
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()
api_url = os.getenv('QDRANT_API_URL')
api_key = os.getenv('QDRANT_API_KEY')

if not api_url:
    raise ValueError("Environment variable 'QDRANT_API_URL' is missing.")
if not api_key:
    raise ValueError("Environment variable 'QDRANT_API_KEY' is missing.")


class QdrantHandler:
    def __init__(self, api_url, api_key, collection_name='pubmed_articles'):
        # Initialize Qdrant client with gRPC timeout options
        self.client = QdrantClient(
            url=api_url,
            api_key=api_key,
            grpc_options=[
                ("grpc.keepalive_timeout_ms", 10000),  # Set timeout for gRPC calls
                ("grpc.keepalive_time_ms", 5000),     # Set keepalive interval
            ]
        )
        self.collection_name = collection_name
        self._initialize_collection()

    def _initialize_collection(self):
        """Ensure the collection exists in Qdrant, otherwise create it."""
        try:
            self.client.get_collection(collection_name=self.collection_name)
            logging.info(f"Collection '{self.collection_name}' exists.")
        except Exception as e:
            logging.info(f"Collection '{self.collection_name}' not found. Creating it.")
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=768, distance=Distance.COSINE)
            )


    def insert_vectors(self, ids, vectors, payloads):
        """
        Insert or update vectors in the Qdrant collection.
        """
        if not (len(ids) == len(vectors) == len(payloads)):
            raise ValueError("Lengths of ids, vectors, and payloads must be the same.")

        try:
            points = [
                {'id': id_, 'vector': vector, 'payload': payload}
                for id_, vector, payload in zip(ids, vectors, payloads)
            ]
            self.client.upsert(collection_name=self.collection_name, points=points)
            logging.info(f"Inserted {len(ids)} vectors into collection '{self.collection_name}'.")
        except UnexpectedResponse as e:
            logging.error(f"Failed to insert vectors: {e}")
            raise  # Re-raise the exception to propagate errors

    def search_vectors(self, query_vector, top_k=5):
        """Search for the top-k most similar vectors in the collection."""
        if len(query_vector) != 768:
            raise ValueError(f"Query vector size must be 768, got {len(query_vector)}")
        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=top_k
            )
            logging.info(f"Search completed. Found {len(results)} results.")
            return results
        except UnexpectedResponse as e:
            logging.error(f"Search failed: {e}")
            return []

    def delete_collection(self):
        """Delete the Qdrant collection."""
        try:
            self.client.delete_collection(collection_name=self.collection_name)
            logging.info(f"Collection '{self.collection_name}' deleted successfully.")
        except UnexpectedResponse as e:
            logging.error(f"Failed to delete collection: {e}")
    def is_collection_empty(self):
        """
        Check if the Qdrant collection is empty.
         """
        try:
            response = self.client.count(self.collection_name)
            return response.get("count", 0) == 0
        except Exception as e:
            logging.error(f"Error checking collection size: {e}")
            return True
    def close_connection(self):
        """Close the Qdrant gRPC connection gracefully."""
        try:
            self.client.grpc_channel.close()
            logging.info("Qdrant gRPC channel closed successfully.")
        except Exception as e:
            logging.error(f"Failed to close Qdrant gRPC channel: {e}")
