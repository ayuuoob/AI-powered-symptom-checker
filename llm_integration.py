def generate_cypher_query(symptoms, schema_info=None):
    """
    Generate a Cypher query based on symptoms and validate against schema.
    """
    print(f"Symptoms Passed to Query: {symptoms}")  # Debugging
    print(f"Schema Info: {schema_info}")  # Debugging

    # Validate symptoms against schema
    if schema_info:
        valid_symptoms = [
            symptom for symptom in symptoms if "Symptom" in schema_info.get("nodes", [])
        ]
    else:
        valid_symptoms = symptoms  # Fall back to all symptoms if no schema is provided

    print(f"Valid Symptoms After Schema Validation: {valid_symptoms}")  # Debugging

    symptom_list = ', '.join(f'"{symptom}"' for symptom in valid_symptoms)
    query = f"""
    MATCH (s:Symptom)<-[:HAS_SYMPTOM]-(d:Disease)-[:TREATED_BY]->(m:Medicine)
    WHERE s.name IN [{symptom_list}]
    RETURN d.name AS disease, m.name AS medicine
    """
    print(f"Generated Query:\n{query}")  # Debugging
    return query

