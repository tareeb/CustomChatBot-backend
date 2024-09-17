import threading
import logging
import chromadb
from django.conf import settings

class ChromaDBConnection:
    _client = None
    _lock = threading.Lock()

    @classmethod
    def get_chromadb_connection(cls):
        with cls._lock:
            if cls._client is None:
                cls._client = cls._create_connection()
            return cls._client

    @classmethod
    def _create_connection(cls):
        try:
            logging.info("Connecting to ChromaDB ...")
            client = chromadb.HttpClient(host=settings.CHROMADB_HOST, port=settings.CHROMADB_PORT)
            logging.info("Successfully connected to ChromaDB.")
            return client
        except Exception as e:
            logging.error(f"Error connecting to ChromaDB: {e}")
            return None

    @classmethod
    def reset_connection(cls):
        with cls._lock:
            cls._client = None
            logging.info("ChromaDB connection has been reset.")