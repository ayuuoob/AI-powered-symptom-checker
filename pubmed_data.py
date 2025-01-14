from Bio import Entrez
import logging
import os
from dotenv import load_dotenv
from embedding_generator import generate_embedding

# Configure logging
logging.basicConfig(level=logging.INFO)

# Set email and API key
load_dotenv()
Entrez.email = "prodigy.hello@gmail.com"  # Replace with your email
Entrez.api_key = os.getenv("ENTREZ_API_KEY")  # Replace with your API key or use environment variables
if not Entrez.api_key:
    logging.error("ENTREZ_API_KEY environment variable is not set.")
    raise EnvironmentError("ENTREZ_API_KEY environment variable is required but not set.")

def fetch_pubmed_data(query, max_results=10):
    """
    Fetch articles from PubMed based on a search query.
    :param query: Search query (e.g., "fever AND treatment")
    :param max_results: Maximum number of articles to retrieve
    :return: List of articles with relevant metadata
    """
    if not query.strip():
        logging.error("Query parameter is empty.")
        return []

    try:
        logging.info(f"Searching PubMed with query: {query}")
        handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
        record = Entrez.read(handle)
        handle.close()

        article_ids = record.get("IdList", [])
        if not article_ids:
            logging.warning("No articles found for the given query.")
            return []

        logging.info(f"Fetched {len(article_ids)} article IDs: {article_ids}")

        # Batch fetch article details
        handle = Entrez.efetch(db="pubmed", id=",".join(article_ids), retmode="xml")
        article_data = Entrez.read(handle)
        handle.close()

        articles = []
        for article in article_data["PubmedArticle"]:
            title = article["MedlineCitation"]["Article"].get("ArticleTitle", "N/A")
            abstract = article["MedlineCitation"]["Article"].get("Abstract", {}).get("AbstractText", "N/A")
            keywords = article["MedlineCitation"].get("KeywordList", [])
            articles.append({
                "id": article["MedlineCitation"]["PMID"],
                "title": title,
                "abstract": " ".join(abstract) if isinstance(abstract, list) else abstract,
                "keywords": [kw for sublist in keywords for kw in sublist] if keywords else []
            })

        logging.info(f"Fetched {len(articles)} articles with details")
        return articles

    except Exception as e:
        logging.error(f"Error fetching data from PubMed: {e}")
        return []

def preprocess_articles(articles):
    """
    Preprocess articles to extract and standardize data.
    """
    processed_data = []
    for article in articles:
        processed_data.append({
            "id": article["id"],
            "title": article["title"].lower(),
            "abstract": article["abstract"].lower(),
            "keywords": [kw.lower() for kw in article["keywords"]],
        })
    return processed_data


def fetch_and_store_pubmed_data(query, qdrant_handler):
    """
    Fetch articles from PubMed and store them in Qdrant.
    """
    if not query.strip():
        logging.warning("Empty query provided. Skipping PubMed fetch.")
        return None

    # Fetch PubMed articles
    pubmed_articles = fetch_pubmed_data(query, max_results=10)
    if not pubmed_articles:
        logging.warning("No articles found in PubMed.")
        return None

    # Preprocess articles
    processed_articles = preprocess_articles(pubmed_articles)

    # Prepare data for Qdrant
    ids = [int(article["id"]) for article in processed_articles]
    vectors = [generate_embedding(article["abstract"]) for article in processed_articles]
    payloads = [{"title": article["title"], "abstract": article["abstract"]} for article in processed_articles]

    # Store in Qdrant
    qdrant_handler.insert_vectors(ids, vectors, payloads)
    logging.info(f"Inserted {len(ids)} PubMed articles into Qdrant.")
    return processed_articles
