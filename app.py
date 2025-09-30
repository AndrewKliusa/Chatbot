# app.py
from flask import Flask, render_template, request, jsonify
import spacy
import sys # For exiting if models aren't found
import os  # For checking if response_logic.py exists

# --- Flask App Setup ---
app = Flask(__name__)

# --- Global SpaCy Model Loading ---
try:
    print("Loading SpaCy English model (en_core_web_sm)...")
    nlp_en = spacy.load("en_core_web_sm")
    print("Loading SpaCy Dutch model (nl_core_news_sm)...")
    nlp_nl = spacy.load("nl_core_news_sm")
    print("SpaCy models loaded successfully!")
except OSError:
    print("\n--- SpaCy Models Not Found! ---")
    print("You need to download the language models first.")
    print("Please run these commands in your terminal:")
    print("  python -m spacy download en_core_web_sm")
    print("  python -m spacy download nl_core_news_sm")
    print("\nThen, please restart the Flask application.")
    sys.exit(1) # Exit the script if models are missing

# --- Import Student's Response Logic ---
if not os.path.exists('response_logic.py'):
    print("\nERROR: 'response_logic.py' not found in the same directory as 'app.py'.")
    print("Please make sure both files are in the same folder.")
    sys.exit(1)
from response_logic import generate_bot_response

# --- Helper Function to get the correct SpaCy model ---
def get_language_model(lang_code: str) -> spacy.language.Language:
    """Returns the appropriate loaded SpaCy model based on the language code."""
    if lang_code == 'en':
        return nlp_en
    elif lang_code == 'nl':
        return nlp_nl
    else:
        # Fallback for unexpected language codes, though we control this in main loop
        print(f"Warning: Unexpected language code '{lang_code}'. Using English model.")
        return nlp_en

# --- Flask Routes ---

@app.route('/')
def home():
    """Renders the main chatbot HTML page."""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handles chat messages from the frontend."""
    user_message = request.json.get('message', '').strip() # type: ignore
    # Get the language chosen by the user from the frontend
    input_lang = request.json.get('lang', 'en') # type: ignore # Default to 'en' if not provided

    if not user_message:
        return jsonify(en_response="Please type something. (Typ iets alsjeblieft.)",
                       nl_response="Please type something. (Typ iets alsjeblieft.)")

    # Process input with the correct SpaCy model based on user's choice
    nlp_model = get_language_model(input_lang)
    doc = nlp_model(user_message)

    # Generate response using the student's logic
    english_response, dutch_response = generate_bot_response(user_message, doc, input_lang)

    # Return the responses as JSON to the frontend
    return jsonify(en_response=english_response, nl_response=dutch_response)

# --- Run the Flask Application ---
if __name__ == '__main__':
    print("\n--- Starting 'The Talking Doorbell' ---")
    print("Open your web browser and go to: http://127.0.0.1:5000/")
    # Debug mode is great for development as it auto-reloads on code changes
    # Set debug=False for production!
    app.run(debug=True)