from neo4j import GraphDatabase

class Neo4jHandler:
    def __init__(self, uri, user, password):
        """
        Initialize the Neo4jHandler with the connection URI, username, and password.
        """
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        """
        Close the Neo4j database connection.
        """
        self._driver.close()

    def query(self, query, parameters=None):
        """
        Execute a Cypher query against the Neo4j database.
        """
        with self._driver.session() as session:
            result = session.run(query, parameters)
            return [record.data() for record in result]

    def get_database_schema(self):
        """
        Retrieve the database schema using Cypher queries.
        """
        try:
            # Get node labels
            node_query = "CALL db.labels()"
            node_result = self.query(node_query)
            nodes = [record["label"] for record in node_result]

            # Get relationship types
            rel_query = "CALL db.relationshipTypes()"
            rel_result = self.query(rel_query)
            relationships = [record["relationshipType"] for record in rel_result]

            return {
                "nodes": nodes,
                "relationships": relationships,
            }
        except Exception as e:
            print(f"Error fetching schema: {e}")
            return None
