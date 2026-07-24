import os 
import threading 

from dotenv import load_dotenv 

try: 
    from google import genai 
    from google.genai import types 
    GENAI_AVAILABLE = True 
except ImportError: 
    GENAI_AVAILABLE = False 

load_dotenv()

DEFAULT_AI = os.getenv("GEMINI_MODEL", "gemini-2.5-flash") 

KEYRING_SERVICE = "TypeRigher"
KEYRING_USER ="gemini_api_key"

_client = None
_client_key = None 

#resolve api key 
def get_api_key(): 

    key = os.getenv("GEMINI_API_KEY")
    if key: 
        return key.strip(), None 
    
    try:
        import keyring 
        key = keyring.get_password(KEYRING_SERVICE, KEYRING_USER)
        if key: 
            return key.strip(), None 
    except Exception as e: 
        return None, f"Could not read keyring: {e}"
    
    return None, "No Gemini API key found. Add one in Settings."

def set_api_key(): 
    #global cashed variables
    global _cilent, _cilent_key 
    try: 
        import keyring 
        keyring.set_password(KEYPRING_SERVICE, KEYRING_USER, key.strip()) #keep into OS

        #reset password
        _cilent = None 
        _cilent_key = None 
        return True, "API key saved."
    except Exception as e: 
        return False, f"Could not Save API key: {e}"
    
def get_cilent(): 
