# response_logic.py
from http.client import responses
from idlelib.rpc import response_queue

import spacy # Imported for type hinting purposes

def generate_bot_response(user_input_text: str, doc: spacy.tokens.doc.Doc, detected_lang: str) -> tuple[str, str]:
    """
    Generates a chatbot response based on user input and SpaCy analysis.
    Students will add their custom rules and responses within this function.

    Args:
        user_input_text (str): The raw text entered by the user.
        doc (spacy.tokens.doc.Doc): The SpaCy processed document of the user input.
                                    Use 'doc' to access tokens, POS tags, etc.
        detected_lang (str): The language code ('en' for English, 'nl' for Dutch)
                             chosen by the user for their input.

    Returns:
        tuple[str, str]: A tuple containing two strings:
                         (English_response_string, Dutch_response_string).
                         The bot will say both.
    """

    # --- Student's Zone: Add your IF-statements and response logic below ---

    # Default responses if no specific rule is matched
    response_en = ""
    response_nl = ""

    # Response Example 1: Example Simple Greeting (works for both English and Dutch greetings) *
    if "hello" in user_input_text.lower() or \
            "hi" in user_input_text.lower() or \
            "hoi" in user_input_text.lower() or \
            "hallo" in user_input_text.lower():
        response_en += "Hello there! Welcome! Who's there?'<br/>"
        response_nl+="Hallo daar! Welkom! Wie is daar?'<br/>"

    # Response example 2: Recognizing a "verb" using SpaCy's Part-of-Speech tag **
    for token in doc:
        if token.pos_ == "VERB": # Check if the word is a Verb
            # We use an f-string to include the user's verb in our response.
            response_en+=f"You used the verb '{token.text}'.<br/>"
            response_nl+=f"Je gebruikte het werkwoord '{token.text}'.<br/>"


    # --- Student Zone ---

    if "thank you" in user_input_text.lower() or \
            "dank je wel" in user_input_text.lower():
        response_en += "It's a pleasure<br/>"
        response_nl+="Alsjeblieft<br/>"

    if "dog" in user_input_text.lower() or "hond" in user_input_text.lower():
        response_en += "Dogs are such loyal animals!<br/>"
        response_nl += "Honden zijn zulke trouwe dieren!<br/>"

    if "cat" in user_input_text.lower() or "kat" in user_input_text.lower():
        response_en += "Cats can be very independent and playful.<br/>"
        response_nl += "Katten kunnen erg onafhankelijk en speels zijn.<br/>"

    if "car" in user_input_text.lower() or "auto" in user_input_text.lower():
        response_en += "Cars make life so much easier for travel.<br/>"
        response_nl += "Auto's maken het reizen zoveel makkelijker.<br/>"

    if "house" in user_input_text.lower() or "huis" in user_input_text.lower():
        response_en += "A house is a cozy place to feel at home.<br/>"
        response_nl += "Een huis is een gezellige plek om je thuis te voelen.<br/>"

    if "yes" in user_input_text.lower() or \
            "yeah" in user_input_text.lower() or \
                "ja" in user_input_text.lower():
        response_en+= f"Great to hear!<br/>"
        response_nl+= f"Goed om te horen!<br/>"

    if "no" in user_input_text.lower() or \
            "nope" in user_input_text.lower() or \
                "nee" in user_input_text.lower():
        response_en+=f"Why not?<br/>"
        response_nl+=f"Waarom niet?<br/>"

    if "please" in user_input_text.lower() or \
            "alstublieft" in user_input_text.lower() or \
                "asjeblieft" in user_input_text.lower():
        response_en+=f"With pleasure!<br/>"
        response_nl+=f"Met plezier!<br/>"

    if "could" in user_input_text.lower() or \
            "can" in user_input_text.lower() or \
                "would" in user_input_text.lower() or \
                    "zou kunnen" in user_input_text.lower() or \
                        "zou" in user_input_text.lower():
        response_en+= f"Sure!, I could help with '{token.text}'.<br/>"
        response_nl+= f"Zeker! Ik kan helpen met '{token.text}'.<br/>"

    if "!" and token.text in user_input_text.lower():
        response_en+= "SIR YES SIR!"
        response_nl+= "MENEER JA MENEER"

    # --- End of Student's Zone ---

    # If none of the above rules match, return the default response.

    return response_en, response_nl
