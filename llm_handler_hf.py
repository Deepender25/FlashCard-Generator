# llm_handler_hf.py
import requests
import demjson3
import logging
import re

# --- CONFIGURATION ---
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
logging.basicConfig(level=logging.INFO)

# --- NEW, MORE RELIABLE FIXER FUNCTION ---
def fix_json_format(raw_text: str) -> str:
    """
    Cleans and attempts to fix common JSON issues from LLM outputs.
    1. Removes text outside the main JSON structure (like "Here are your cards:").
    2. Fixes the common error of a missing closing brace '}' for the last item in a list.
    """
    # 1. Find the start of the JSON list
    start_bracket = raw_text.find('[')
    if start_bracket == -1:
        logging.error("No opening bracket '[' found in the response.")
        return raw_text # Return as is if no JSON list is found
    
    # 2. Find the end of the JSON list
    end_bracket = raw_text.rfind(']')
    if end_bracket == -1:
        logging.error("No closing bracket ']' found in the response.")
        return raw_text

    # 3. Extract the JSON part
    json_part = raw_text[start_bracket : end_bracket + 1]

    # 4. The "missing brace" fix:
    # If the text right before the final ']' is a double quote (with optional whitespace),
    # it's highly likely the object wasn't closed.
    # Regex: looks for a '"', optional whitespace, then the final ']'
    pattern = r'"\s*\]$' 
    if re.search(pattern, json_part.strip()):
        # Insert the missing '}'
        fixed_json = json_part.strip()[:-1] + "}]"
        logging.warning("Detected and fixed a missing closing brace '}' in the JSON response.")
        return fixed_json

    return json_part


# --- MAIN FUNCTION ---
def generate_flashcards_hf(api_token, text, num_cards=10, subject="general"):
    """
    Generates flashcards using the Hugging Face Inference API.
    """
    headers = {"Authorization": f"Bearer {api_token}"}
    
    prompt = f"""<|system|>
You are an expert flashcard creator. Your task is to generate exactly {num_cards} question-answer flashcards based on the provided text.
Your entire response MUST be a single, valid JSON list of objects. Each object must have a "question" key and an "answer" key.
Do not add any introduction, explanation, or any text outside of the main JSON list.
Your response must start with '[' and end with ']'.</s>
<|user|>
Generate flashcards for the following text on the subject of '{subject}':
---
{text}
---</s>
<|assistant|>
"""
    # Note: Removed the priming '[' from here to simplify the logic.
    # The model should be good enough to start with it given the instructions.

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 4096,
            "temperature": 0.5,
            "return_full_text": False,
        }
    }

    try:
        logging.info("Sending request to Hugging Face API...")
        response = requests.post(API_URL, headers=headers, json=payload, timeout=180)

        if response.status_code == 503:
            return None, "Model is currently loading on Hugging Face. Please try again in a minute."

        response.raise_for_status()
        result = response.json()
        
        if not result or not isinstance(result, list) or 'generated_text' not in result[0]:
             return None, f"Received an unexpected response format from the API: {result}"

        generated_text = result[0]['generated_text']
        logging.info(f"Received raw response from HF: {generated_text}")

        # Apply our robust fixer before attempting to parse
        fixed_text = fix_json_format(generated_text)
        logging.info(f"Text after cleaning/fixing: {fixed_text}")

        try:
            flashcards = demjson3.decode(fixed_text)
            
            if not isinstance(flashcards, list):
                raise TypeError("Parsed JSON is not a list.")

            return flashcards, None
        except (demjson3.JSONDecodeError, TypeError) as e:
            return None, f"Failed to decode a valid list of flashcards from the AI's response. Error: {e}. Raw text was: {generated_text}"

    except requests.exceptions.RequestException as e:
        return None, f"Hugging Face API request failed: {e}"
    except Exception as e:
        return None, f"An unexpected error occurred: {e}"