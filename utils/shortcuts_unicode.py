import json 
import os 
import sys 
import threading 
import pyperclip

#creates local file (windows)
def _data_dir(): 
    app = "TypeRighter"
    if sys.platform !="win32":
        raise NotImplementedError("This function is currently only implemented for Windows.")
    
    base = os.environ.get("APPDATA", os.path.expanduser("~"))
    folder = os.path.join(base, app)
    os.makedirs(folder, exist_ok=True)
    return folder

def _templates_dir(curr_user): 
    app = "TypeRighter"
    user_folder = curr_user
    templates_folder = "templates"
    if sys.platform !="win32":
        raise NotImplementedError("This function is currently only implemented for Windows.")
    
    base = os.environ.get("APPDATA", os.path.expanduser("~"))
    folder = os.path.join(base, app, user_folder, templates_folder)
    os.makedirs(folder, exist_ok=True)
    return folder
    
DEFAULT_BINDINGS = {
    "unicode": {
        "`": "Exit App",
        "a": "Close Overlay",
        "s": "Control Panel",
        "\\": "Breakout Key",
        "=": "Change Template",
    },
    "latex": {
        "0": {"name": "Fraction", "code": r"\frac{a}{b}"},
        "1": {"name": "3x3 Identity Matrix", "code": r"\begin{pmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{pmatrix}"}
    }
}
_PATH = os.path.join(_data_dir(), "shortcuts.json")
_lock = threading.Lock()

bindings = {}

PROTECTED_BINDS = ["Exit App", "Close Overlay", "Control Panel", "Breakout Key"]

def _norm(key): 
    if key is None: 
        key = ""
    key = key.strip().lower()
    return key 

#load from file 
def load(): 
    global bindings
    with _lock: 
        if os.path.exists(_PATH):
            try: 
                with open(_PATH, "r", encoding="utf-8") as f:
                    bindings = json.load(f)
            except (json.JSONDecodeError, IOError):
                bindings = {}
        else:
            # Create a new file, and add in the default binds
            bindings = DEFAULT_BINDINGS
            temp = _PATH + ".tmp" 
            with open(temp, "w", encoding="utf-8") as f:
                json.dump(bindings, f, ensure_ascii=False, indent=4)
            os.replace(temp, _PATH)
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
    
# for UI to refresh live
_refresh_list = []

def refresh(callback): 
    if callback not in _refresh_list: 
        _refresh_list.append(callback)

def unlist(callback): 
    if callback in _refresh_list: 
        _refresh_list.remove(callback)

#lets listeners re-render
def _notify():
    for callback in list(_refresh_list): 
        try: 
            callback()
        except Exception: 
            pass

def check_binding(key, symbol): 
    if key is None: 
        key = ""
    key = key.lower()

    if not key: 
        return "error", "Please enter a key or phrase"
    if not symbol: 
        return "error", "Invalid Symbol for Binding"
        
    with _lock: 
        existing = (bindings.get("unicode") or {}).get(key)

        #if different symbol
        if existing is not None and existing in PROTECTED_BINDS:
            return "protected", f"'{key}' is bound to the protected command '{existing}'"

        if existing is not None and existing != symbol: 
            return "conflict", f"'{key}' is already bound to '{existing}'"
        
        #if completely free and safe to bind 
        return "ok",""

#binds key to symbol (note: upper & lower treated same)
def set_unicode_binding(key, symbol, overwrite = True):
    if key is None: 
        key =""
    key = key.lower()

    if not key: 
        return False, "Please enter a key or phrase"
    
    if not symbol: 
        return False, "Invalid symbol for binding."
    
    with _lock: 
        unicode_shortcuts = bindings.get("unicode")

        if unicode_shortcuts is None: 
            unicode_shortcuts = bindings["unicode"] = {}
        
        existing = unicode_shortcuts.get(key)
        if existing is not None and existing != symbol and not overwrite: 
            return False, f"'{key}' is already bound to '{existing}'."
        
        unicode_shortcuts[key] = symbol 
        ok = _save()

    if ok: 
        return True, f"Successfully bound '{symbol}' to '{key}'."
    else: 
        return False, f"Failed to bind '{symbol}' to '{key}'. Please try again."

def set_latex_shortcut(latex_code, name):

    # First generate a new unique key for this LaTeX Shortcut
    key = 0 # key is 0 if there arent any shortcuts yet
    curr_latex_shortcuts = all_latex_shortcuts()
    if curr_latex_shortcuts:
        # If there are existing shortcuts, just increment the highest key
        key = str(max(map(int, curr_latex_shortcuts.keys())) + 1)
    
    with _lock: 
        latex_shortcuts = bindings.get("latex")
        latex_shortcuts[key] = {
            "name": name,
            "code": latex_code,
        }
        ok = _save()

    if ok: 
        return True, f"Successfully bound '{latex_code}' with name '{name}'."
    else: 
        return False, f"Failed to bind '{latex_code}' with name '{name}'. Please try again."

#unbind 
def remove_unicode_binding(key): 
    if key == None:
        key =""
    key = key.lower()

    with _lock:
        unicode_shortcuts = bindings.get("unicode")
        if key in unicode_shortcuts: 
            binded = True
            del unicode_shortcuts[key]

        else: 
            binded = False

    if binded:
        _save()
    return binded

def remove_latex_shortcut(key): 
    if key == None:
        key =""
    key = key.lower()

    with _lock:
        latex_shortcuts = bindings.get("latex")
        if key in latex_shortcuts: 
            binded = True
            del latex_shortcuts[key]

        else: 
            binded = False

    if binded:
        _save()
    return binded

#read symbol binded to key
def lookup_unicode(key): 
    if key == None:
        key =""
    key = key.lower()
 
    with _lock:
        unicode_shortcuts = bindings.get("unicode")
        return unicode_shortcuts.get(key)

def get_key_from_value(value):

    with _lock:
        unicode_shortcuts = bindings.get("unicode")
        # Assume each value only has one unique key
        key = next((k for k, v in unicode_shortcuts.items() if v == value), None)

        if not key:
            return None
        else:
            return key
    
#shows all bindings 
def all_bindings():
    with _lock:
        return dict(bindings)

def all_unicode_bindings(): 
    with _lock: 
        return dict(bindings.get("unicode"))
    
def all_key_bindings(): 
    with _lock: 
        return {k: v for k, v in (bindings.get("unicode") or {}).items() if len(k) == 1}
    
def all_phrase_bindings(): 
    with _lock:
        return {k: v for k, v in (bindings.get("unicode") or {}).items() if len(k) > 1}
                
def all_latex_shortcuts():
    with _lock:
        return dict(bindings.get("latex"))

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
    symbol = lookup_unicode(text)
    if symbol is None: 
        return None 
    
    success = copy_to_clipboard(symbol)

    if success: 
        return symbol
    else:
        return None