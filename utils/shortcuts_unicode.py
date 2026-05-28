import json 
import os 
import sys 
import threading 
from pynput import keyboard
import pyperclip

#creates local file (windows)
def _data_dir(): 
    app = "TypeRighter"
    if sys.platform == "win32": 
        base = os.environ.get("APPDATA", os.path.expanduser("~"))

        folder = os.path.join(base, app)
        os.makedirs(folder, exist_ok=True)
        return folder
    
_PATH = os.path.join(_data_dir(), "shortcuts_unicode.json")
_lock = threading.Lock()

bindings = {}

RESERVED_KEYS ={"a", "\\", "`", keyboard.Key.esc}

#load from file 
def _load(): 
    global bindings
    with _lock: 
        if os.path.exists(_PATH):
            try: 
                with open(_PATH, "r", encoding="utf-8") as f:
                    bindings = json.load(f)
            except (json.JSONDecodeError, IOError):
                bindings = {}
        else: 
            bindings = {}
        return dict(bindings) #copy of bindings

#save to file
def _save(): 
    try: 
        temp = _PATH + ".tmp" 
        with open(temp, "w", encoding="utf-8") as f:
            json.dump(bindings, f, ensure_ascii=False, indent=4)
        os.replace(temp, _PATH)
        return True #saved successfully
    except IOError:
        return False 

#binds key to symbol (note: upper & lower treated same)
def set_binding(key, symbol):
    if key is None: 
        key =""
    else: 
        key = key 
    key = key.lower()

    if len(key) != 1:
        return False, "Please enter a single character key." 
    if key in RESERVED_KEYS: 
        return False, f"'{key}' is reserved and cannot be used as a shortcut key."
    if not symbol: 
        return False, "Invalid symbol for binding."
    
    with _lock: 
        bindings[key] = symbol 
        ok = _save()

    if ok: 
        return True, f"Successfully bound '{symbol}' to '{key}'."
    else: 
        return False, f"Failed to bind '{symbol}' to '{key}'. Please try again."

#unbind 
def remove_binding(key): 
    if key == None:
        key =""
    else: 
        key = key
    key = key.lower()

    with _lock: 
        if key in bindings: 
            binded = True

            symbol = bindings[key]
            del bindings[key]

        else: 
            binded = False

    if binded:
        _save()

#read symbol binded to key
def lookup(key): 
    if key == None:
        key =""
    else: 
        key = key
    key = key.lower()

    with _lock: 
        return bindings.get(key)
    
#shows all bindings 
def all_bindings(): 
    with _lock: 
        return dict(bindings)
    

#copy to clipboard 
def copy_to_clipboard(text):
    if not text: 
        return False 
    try:
        pyperclip.copy(text)
        return True
    except pyperclip.PyperclipException:
        return False 
    
def copy_symbol(text): 
    symbol = lookup(text)
    if symbol is None: 
        return None 
    
    success = copy_to_clipboard(symbol)

    if success: 
        return symbol
    else:
        return None