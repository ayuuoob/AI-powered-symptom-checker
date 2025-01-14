def extract_symptoms(user_input):
    """
    Extract symptoms from user input using keyword matching based on a predefined list.
    """
    # List of possible symptoms (all converted to lowercase for consistency)
    possible_symptoms = [
        "fever", "cough", "fatigue", "difficulty breathing", "wheezing", "chest pain",
        "high blood sugar", "nausea", "sensitivity to light", "headache", "joint pain",
        "swelling", "persistent cough", "weight loss", "brain damage", "memory loss",
        "cognitive decline", "indigestion", "mucus production", "seizures",
        "liver inflammation", "bone fractures", "skin itchiness", "skin patches",
        "abdominal pain", "excessive worry", "sadness", "redness", "autoimmune reaction"
    ]

    # Normalize input to lowercase and split it into words
    user_input = user_input.lower()

    # Extract symptoms by checking which possible symptoms are mentioned in the input
    extracted = [symptom for symptom in possible_symptoms if symptom in user_input]

    return extracted

def get_user_input(user_input):
    """
    Prompt the user to describe their symptoms.
    """
    symptoms = extract_symptoms(user_input)
    print(f"Raw User Input: {user_input}")  # Debugging
    print(f"Extracted Symptoms: {symptoms}")  # Debugging
    return symptoms

def display_results(results):
    """
    Display the results of the diagnosis and treatment options.
    """
    if not results:
        print("No results found. Please consult a medical professional.")
        return

    print("\nPossible diagnoses and treatments:")
    for record in results:
        print(f"- Disease: {record['disease']}, Medicine: {record['medicine']}")
