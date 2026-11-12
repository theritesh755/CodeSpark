from neo4j import GraphDatabase
from config.settings import settings

def get_neo4j_driver():
    return GraphDatabase.driver(settings.NEO4J_URI, auth=(settings.NEO4J_USERNAME, settings.NEO4J_PASSWORD))
