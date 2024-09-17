import os
import threading
from dotenv import load_dotenv
from langchain_community.graphs import Neo4jGraph

# Load environment variables from .env file at the start
load_dotenv()

class Neo4jConnection:
    _graph = None
    _lock = threading.Lock()

    @classmethod
    def get_neo4j_connection(cls):
        with cls._lock:
            if cls._graph is None:
                cls._graph = cls._create_connection()
            return cls._graph

    @classmethod
    def _create_connection(cls):
        try:
            print("Connecting to Neo4j...")
            url = os.environ.get("NEO4J_URL")
            username = os.environ.get("NEO4J_USERNAME", "neo4j")  # default username if not set in env
            password = os.environ.get("NEO4J_PASSWORD")

            if not url or not password:
                print("Missing Neo4j environment variables.")
                return None

            graph = Neo4jGraph(
                url=url,
                username=username,
                password=password
            )
            print("Successfully connected to Neo4j.")
            return graph
        except Exception as e:
            print(f"Error connecting to Neo4j: {e}")
            return None

    @classmethod
    def reset_connection(cls):
        with cls._lock:
            cls._graph = None
            print("Neo4j connection has been reset.")
