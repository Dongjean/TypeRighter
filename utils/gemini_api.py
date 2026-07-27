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

DEFAULT_AI = os.getenv("GEMINI_MODEL_main", "gemini-flash-latest")
BACKUP_MODELS = [
    os.getenv("GEMINI_MODEL_backup_1"),
    os.getenv("GEMINI_MODEL_backup_2"),
    os.getenv("GEMINI_MODEL_backup_3")
]
print(f">>> MODEL IN USE: {repr(DEFAULT_AI)}")

KEYRING_SERVICE = "TypeRighter"
KEYRING_USER ="gemini_api_key"

_client = None
_client_key = None 

#get API key in .env (our API key - internal)
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

#save API key (if users providing - future extension)
def set_api_key(key): 
    #global cashed variables
    global _client, _client_key 
    try: 
        import keyring 
        keyring.set_password(KEYRING_SERVICE, KEYRING_USER, key.strip()) #keep into OS

        #reset password
        _client = None 
        _client_key = None 
        return True, "API key saved."
    except Exception as e: 
        return False, f"Could not Save API key: {e}"

#initialise client connection using key     
def get_client(): 
    global _client, _client_key 

    if not GENAI_AVAILABLE: 
        return None, "Gemini is not installed. Run: pip install google-genai"
    
    key, e = get_api_key() 
    if e: 
        return None, e 
    
    #if key changed, create new client and stored 
    if _client is None or _client_key != key:
        try: 
            _client = genai.Client(api_key=key) 
            _client_key = key 

        except Exception as e: 
            _client = None 
            return None, f" Could not create Gemini Client: {e}"

    return _client, None

def try_backup_models(client, prompt, config_kwargs):
    global DEFAULT_AI
    print("Using backup AI Model...")
    try:
        for BACKUP_MODEL in BACKUP_MODELS:
            response = client.models.generate_content(
                model = BACKUP_MODEL, 
                contents = prompt, 
                config = types.GenerateContentConfig(**config_kwargs), 
            )
            msg = None
            # Use the first response that works
            print(f"used {BACKUP_MODEL} for prompt {prompt}")
            DEFAULT_AI = BACKUP_MODEL
            print(f"using {DEFAULT_AI} as the main AI now.")
            break
    except Exception as e: 
        response = None
        msg = str(e) 

    return response, msg

#actual network request to API and processing
def generate(prompt, system_instruction = None, schema = None, model = None, temperature = 0.1): 
    client, e = get_client()
    if e: 
        return False, e 
    
    config_kwargs = {"temperature": temperature }
    if system_instruction: 
        config_kwargs["system_instruction"] = system_instruction
    if schema: 
        config_kwargs["response_mime_type"] = "application/json"
        config_kwargs["response_schema"] = schema 

    try: 
        response = client.models.generate_content(
            model = model or DEFAULT_AI, 
            contents = prompt, 
            config = types.GenerateContentConfig(**config_kwargs), 
        )
        msg = None
    except Exception as e: 
        msg = str(e)

        if "429" in msg or "RESOURCE_EXHAUSTED" in msg:
            if "per day" in msg.lower() or "PerDay" in msg:

                # If main AI model requests per day is exhausted, try the backups
                response_backup, msg_backup = try_backup_models(client, prompt, config_kwargs)

                if not response_backup:
                    return False, "Daily AI quota used up. Resets at midnight"

            if not response_backup:
                return False, "Too many requests. Wait a minute and try again"
        if "API_KEY_INVALID" in msg or "401" in msg or "403" in msg and not response_backup: 
            return False, "Gemini API key was rejected. Check GEMINI_API_KEY in .env."
        
        #if none of the errors mentioned above
        if not response_backup:
            return False, f"Gemini request failed: {msg}"

    # Try using the backup response if it exists
    try:
        response = response_backup
    except Exception as e:
        pass

    text = getattr(response, "text", None)
    if not text: 
        return False, "Gemini returned an empty response."
    return True, text

def generate_async(widget, prompt, on_done, system_instruction = None, schema = None, model = None, temperature =0.2): 
    #create a different working thread
    def worker():
        ok,result = generate( 
            prompt, 
            system_instruction=system_instruction, 
            schema=schema, 
            model = model, 
            temperature = temperature, 
        )
        
        try: 
            widget.after(0, lambda: on_done(ok,result))
        except Exception: 
            pass 
    threading.Thread(target=worker, daemon = True).start()

