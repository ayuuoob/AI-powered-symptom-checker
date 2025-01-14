# AI-powered-symptom-checker
# **MedHelp - AI-Powered Health Assistant**

MedHelp is an AI-powered chatbot designed to assist users with health-related queries. Using natural language processing, the chatbot provides:

- **Symptom Analysis**: Extracts symptoms from user input and matches them with possible diseases.
- **Medical Recommendations**: Suggests over-the-counter medications and advises consulting appropriate specialists.
- **Conversational Support**: Generates empathetic, human-like responses.

---

## **Key Features**
- **Multi-Source Data Integration**: Combines data from Neo4j, Qdrant, and PubMed for accurate and comprehensive responses.
- **Web-Based Interface**: User-friendly chat interface with dynamic message bubbles and a modern design.
- **Structured Responses**: Provides actionable insights in a clear, organized format, including possible diseases, medications, and doctor recommendations.
- **Interactive Experience**: Handles user queries seamlessly and provides conversational responses in real-time.

---

## **Technologies Used**
### **Frontend**
- HTML, CSS, JavaScript
- Dynamic message formatting and animations for a better user experience.

### **Backend**
- Flask (Python)
- Integration with:
  - Neo4j: For knowledge graphs.
  - Qdrant: For semantic search.
  - PubMed: For medical research data.

### **AI Model**
- Uses **Gemini** for generating human-like, empathetic responses.

---

## **Setup Instructions**
Follow these steps to set up the project locally:

1. **Clone the Repository**:
git clone https://github.com/your-username/MedHelp.git cd MedHelp

markdown
Copier le code

2. **Create and Activate a Virtual Environment**:
python -m venv venv source venv/bin/activate # On macOS/Linux venv\Scripts\activate # On Windows

markdown
Copier le code

3. **Install Dependencies**:
pip install -r requirements.txt

markdown
Copier le code

4. **Run the Flask Application**:
python app.py

markdown
Copier le code

5. **Access the Application**:
Open your browser and navigate to:
http://127.0.0.1:5000/

---

## **How It Works**
1. **User Interaction**: The user inputs symptoms or health-related queries through the chatbot interface.
2. **AI Processing**:
- Extracts symptoms using natural language processing (NLP).
- Queries Neo4j, Qdrant, and PubMed for relevant information.
- Generates a structured, conversational response.
3. **Dynamic Display**: The response is displayed in a visually appealing, easy-to-read format.
