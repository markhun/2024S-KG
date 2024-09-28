from neo4j import GraphDatabase

# URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
URI = "bolt://localhost:7687"
AUTH = ("neo4j", "password")


def run_query(query, params={}):
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        result = driver.execute_query(query, params)
        return result
