import logging
import os
from flask import Flask, request, jsonify,render_template
from database import Neo4jHandler
from qdrant_handler import QdrantHandler
from huggingface_integration import SymptomAnalyzer
from embedding_generator import generate_embedding
from pubmed_data import fetch_and_store_pubmed_data
from dotenv import load_dotenv
from llm_integration import generate_cypher_query

# Load environment variables
load_dotenv()

# Logging configuration
logging.basicConfig(level=logging.INFO)

# Flask application
app = Flask(__name__)

# Initialize global components
neo4j_handler = Neo4jHandler(
    os.getenv("NEO4J_URI"),
    os.getenv("NEO4J_USER"),
    os.getenv("NEO4J_PASSWORD")
)
qdrant_handler = QdrantHandler(
    api_url=os.getenv("QDRANT_API_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)
analyzer = SymptomAnalyzer(api_key=os.getenv("ANALYZER_API_KEY"))

@app.route('/')
def index():
    return render_template('index.html')

# Chatbot route for web-based interaction
@app.route('/chat', methods=['POST'])
def chat():
    """
    Handle user messages via HTTP POST and return AI-generated responses.
    """
    try:
        user_input = request.json.get("message")
        if not user_input:
            return jsonify({"error": "No message provided"}), 400

        # Process user input
        symptoms = analyzer.extract_symptoms(user_input)
        if symptoms:
            response = process_symptoms(symptoms, neo4j_handler, qdrant_handler, analyzer)
        else:
            response = analyzer.generate_conversational_response(user_input)

        return jsonify({"response": response})

    except Exception as e:
        logging.error(f"Error in chat route: {e}")
        return jsonify({"error": str(e)}), 500

# Chatbot CLI loop
def chatbot_loop(neo4j_handler, qdrant_handler, analyzer):
    """
    Conversational loop for the AI chatbot in CLI mode.
    """
    print("Hi! I'm here to help. How are you feeling today?")
    while True:
        # Get user input
        user_input = input("You: ").strip()
        if user_input.lower() in {"exit", "quit", "bye"}:
            print("It was nice talking to you! Take care and feel better soon.")
            break

        # Process input
        try:
            symptoms = analyzer.extract_symptoms(user_input)
            if symptoms:
                print("Let me look into this for you...")
                response = process_symptoms(symptoms, neo4j_handler, qdrant_handler, analyzer)
            else:
                response = analyzer.generate_conversational_response(user_input)
            print(f"AI: {response}")
        except Exception as e:
            print("I'm sorry, something went wrong. Could you please try again?")
            logging.error(f"Error in chatbot loop: {e}")

# Process symptoms
def process_symptoms(symptoms, neo4j_handler, qdrant_handler, analyzer):
    """
    Process symptoms to query Neo4j, Qdrant, and PubMed, then generate a combined response.
    """
    combined_results = []

    # Step 1: Query Neo4j
    neo4j_results = query_neo4j(symptoms, neo4j_handler)
    if neo4j_results:
        combined_results.extend([
            {"source": "Neo4j", "data": result} for result in neo4j_results
        ])

    # Step 2: Semantic search in Qdrant
    query_embedding = generate_embedding(" ".join(symptoms))
    qdrant_results = qdrant_handler.search_vectors(query_embedding, top_k=5)
    if qdrant_results:
        combined_results.extend([
            {"source": "Qdrant", "data": {"title": res.payload.get("title"), "abstract": res.payload.get("abstract")}}
            for res in qdrant_results
        ])

    # Step 3: Fetch data from PubMed
    pubmed_results = fetch_and_store_pubmed_data(" ".join(symptoms), qdrant_handler)
    if pubmed_results:
        combined_results.extend([
            {"source": "PubMed", "data": article} for article in pubmed_results
        ])

    # Step 4: Use Gemini to analyze and generate the response
    if combined_results:
        return analyzer.generate_combined_response(combined_results, symptoms)
    else:
        return "I'm sorry, I couldn't find much information. Please consult a healthcare professional."

# Query Neo4j
def query_neo4j(symptoms, neo4j_handler):
    """
    Generate and execute a Cypher query for Neo4j.
    """
    try:
        query = generate_cypher_query(symptoms)
        logging.debug(f"Generated Cypher Query: {query}")
        return neo4j_handler.query(query)
    except Exception as e:
        logging.error(f"Neo4j query failed: {e}")
        return None

# Main entry point
if __name__ == "__main__":
    import sys

    # Determine if running in CLI mode or Flask mode
    if len(sys.argv) > 1 and sys.argv[1] == "cli":
        chatbot_loop(neo4j_handler, qdrant_handler, analyzer)
    else:
        app.run(debug=True)
