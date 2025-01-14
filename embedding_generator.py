from sentence_transformers import SentenceTransformer
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize the SentenceTransformer model
model_name = "cambridgeltl/SapBERT-from-PubMedBERT-fulltext"  # Specify your desired model
embedding_model = SentenceTransformer(model_name)

def generate_embedding(text):
    """
    Generate a vector embedding for a given text using a pre-trained model.

    Args:
        text (str): The input text for which to generate the embedding.

    Returns:
        list[float]: The embedding vector as a list of floats.
    """
    if not text:
        raise ValueError("Input text cannot be empty")

    logging.info(f"Generating embedding for text: {text[:50]}...")
    embedding = embedding_model.encode(text, convert_to_numpy=True).tolist()
    logging.info("Embedding generated successfully")
    return embedding

def generate_embeddings(texts):
    """
    Generate embeddings for multiple texts in a batch.
    Args:
        texts (list[str]): A list of input texts.

    Returns:
        list[list[float]]: A list of embeddings, one for each input text.
    """
    if not texts:
        raise ValueError("Input texts cannot be empty")

    logging.info(f"Generating embeddings for {len(texts)} texts...")
    embeddings = embedding_model.encode(texts, convert_to_numpy=True).tolist()
    logging.info("Batch embeddings generated successfully")
    return embeddings
