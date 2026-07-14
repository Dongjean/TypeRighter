import json 
import os 
import sys 
import threading 
import pyperclip

import utils.templates as templates

#creates local file (windows)
def _data_dir(): 
    app = "TypeRighter"
    if sys.platform !="win32":
        raise NotImplementedError("This function is currently only implemented for Windows.")
    
    base = os.environ.get("APPDATA", os.path.expanduser("~"))
    folder = os.path.join(base, app)
    os.makedirs(folder, exist_ok=True)
    return folder

#creates local file (windows)
def _user_dir(curr_user): 
    app = "TypeRighter"
    user_folder = curr_user
    if sys.platform !="win32":
        raise NotImplementedError("This function is currently only implemented for Windows.")
    
    base = os.environ.get("APPDATA", os.path.expanduser("~"))
    folder = os.path.join(base, app, user_folder)
    os.makedirs(folder, exist_ok=True)
    return folder

_PATH = os.path.join(_data_dir(), "settings.json")
_lock = threading.Lock()

DEFAULT_SETTINGS = {
    "curr_template": "default"
}

settings = DEFAULT_SETTINGS

#load from file
def load(curr_user): 
    global settings
    with _lock:


        # If we are logged in, pull the latest settings of the curr_user
        if curr_user:
            if os.path.exists(_PATH):
                try: 
                    with open(_PATH, "r", encoding="utf-8") as f:
                        settings = json.load(f)
                except (json.JSONDecodeError, IOError):
                    settings = {}
            else:
                # Create a new file, and add in the default settings
                settings = DEFAULT_SETTINGS
                temp = _PATH + ".tmp" 
                with open(temp, "w", encoding="utf-8") as f:
                    json.dump(settings, f, ensure_ascii=False, indent=4)
                os.replace(temp, _PATH)
            
        temp = _PATH + ".tmp"
        with open(temp, "w", encoding="utf-8") as f:
            json.dump(settings, f, ensure_ascii=False, indent=4)
        os.replace(temp, _PATH)
        
        return dict(settings) #copy of settings

#save to file
def _save(): 
    try: 
        temp = _PATH + ".tmp" 
        with open(temp, "w", encoding="utf-8") as f:
            json.dump(settings, f, ensure_ascii=False, indent=4)
        os.replace(temp, _PATH)
        return True #saved successfully
    except IOError:
        return False 

#sets a new setting
def set_setting(setting_id, new_setting):
    
    with _lock: 
        settings[setting_id] = new_setting 
        ok = _save()

    if ok: 
        return True, f"Successfully set '{setting_id}' to '{new_setting}'."
    else: 
        return False, f"Failed to set '{setting_id}' to '{new_setting}'. Please try again."

#read a setting
def lookup_setting(setting_id): 
 
    with _lock:
        return settings.get(setting_id)

#shows all settings
def all_settings(): 
    
    with _lock:
        return dict(settings)