from django.apps import AppConfig
from utils.ChromaConnection import ChromaDBConnection 

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        ChromaDBConnection.get_chromadb_connection()