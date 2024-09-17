import requests
import os
import logging

session = None

def get_llm_guard_session():
    """Lazily initializes and returns a persistent session."""
    global session
    if session is None:
        session = requests.Session() 
    return session

def LLMGuard(input_text):
    try:
        llm_guard_session = get_llm_guard_session()

        response = llm_guard_session.post(
            "https://api.lakera.ai/v1/prompt_injection",
            json={"input": input_text},
            headers={"Authorization": f'Bearer {os.environ.get("LAKERA_API_KEY")}'},
            timeout=10
        )

        if response.status_code == 200:
            response_json = response.json()
            flag = response_json["results"][0]["flagged"]
            logging.info(f"LLM Guard : {flag}")
            return flag
        else:
            logging.error(f"LLMGuard API returned non-200 status: {response.status_code}")
            return False

    except requests.exceptions.RequestException as e:
        logging.error(f"Error connecting to LLMGuard API: {e}")
        return False
