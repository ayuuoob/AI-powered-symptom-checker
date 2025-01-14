import google.generativeai as genai
import logging


class SymptomAnalyzer:
    def __init__(self, api_key, model_name="gemini-1.5-flash"):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    def extract_symptoms(self, user_input):
        """
        Use Gemini to extract symptoms from user input.
        """
        prompt = (
            f"The user said: '{user_input}'. "
            "Extract symptoms if present; otherwise, return an empty list."
        )
        response = self.model.generate_content(prompt)
        try:
            return eval(response.text)  # Assuming response is a Python-style list
        except Exception as e:
            logging.error(f"Error parsing symptom extraction response: {e}")
            return []

    def generate_conversational_response(self, user_input):
        """
        Generate a conversational response if no symptoms are found.
        """
        prompt = f"The user said: '{user_input}'. Generate a friendly response."
        response = self.model.generate_content(prompt)
        return response.text

    def generate_response_from_pubmed(self, articles):
        """
        Generate a conversational response based on PubMed articles.
        """
        summary = "\n".join(
            f"- {article['title']}: {article['abstract'][:200]}..."
            for article in articles
        )
        prompt = (
            f"The user reported symptoms, and the following PubMed articles were retrieved:\n{summary}\n\n"
            "Generate a conversational summary for the user."
        )
        response = self.model.generate_content(prompt)
        return response.text
    def generate_response(self, results):
        """
        Generate a conversational response based on Neo4j query results.
        """
     # Group medications by disease for better presentation
        disease_medication_map = {}
        for record in results:
            disease = record.get('disease', 'Unknown Disease')
            medicine = record.get('medicine', 'Unknown Medicine')
            if disease not in disease_medication_map:
                disease_medication_map[disease] = []
            disease_medication_map[disease].append(medicine)

        # Create a summary of diseases and medications
        summary = "\n".join(
            f"- {disease}: {', '.join(set(medicines))}"  # Use `set` to avoid duplicate medicines
            for disease, medicines in disease_medication_map.items()
        )

    # AI prompt for conversational response
        prompt = (
            f"The following diseases and treatments were identified based on the user's symptoms:\n{summary}\n\n"
            "Please generate a conversational response that summarizes this information and emphasizes consulting a healthcare professional."
        )
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logging.error(f"Error generating response: {e}")
            return "I'm sorry, but I couldn't generate a response. Please consult a healthcare professional."
    def generate_combined_response(self, combined_results, symptoms):
        """
        Generate a conversational response by filtering and summarizing combined results.
        """
        # Format the results for Gemini
        results_summary = "\n".join([
            f"- Source: {item['source']}\n  Title: {item['data'].get('title', 'N/A')}\n  Abstract: {item['data'].get('abstract', 'N/A')[:200]}..."
            for item in combined_results
        ])

    # Create the prompt for Gemini
        prompt = (
            f"The user reported the following symptoms: {', '.join(symptoms)}.\n\n"
            f"I found the following relevant information from various sources:\n{results_summary}\n\n"
            "Based on the symptoms and information, generate a structured response in the following format:\n"
            "1. **Possible Diseases**:\n"
            "   - Provide a list of possible diseases the user might have, with brief descriptions if available.\n"
            "2. **Recommended Medications**:\n"
            "   - List over-the-counter or commonly prescribed medications that could help manage the symptoms. Include a note to consult a doctor before use.\n"
            "3. **Suggested Specialist**:\n"
            "   - Recommend the type of doctor the user should consult (e.g., general practitioner, neurologist).\n\n"
            "The response should be conversational, empathetic, and helpful. Avoid chatbot-like language. Ensure the output is concise, clear, and easy to read."
)


        try:
        # Generate the response using Gemini
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logging.error(f"Error generating combined response: {e}")
            return "I'm sorry, but I couldn't generate a response. Please consult a healthcare professional."