import json 
import os 
import sys 
import threading 
import pyperclip

import utils.templates as templates
import utils.firebase_app as fb

db = fb.db

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
def load(curr_user, pull_fb=False): 
    global settings

    if pull_fb:
        try:
            user_settings_ref = db.collection("settings")
            all_settings = user_settings_ref.get_document(curr_user)
        except:
            pass
    
    with _lock:

        # If we successfully pulled settings data from firebase, write to file
        if pull_fb and all_settings:
            settings = all_settings
            temp = _PATH + ".tmp" 
            try:
                with open(temp, "w", encoding="utf-8") as f:
                    json.dump(settings, f, ensure_ascii=False, indent=4)
                os.replace(temp, _PATH)
            except:
                return False
        
        # If firebase has no valid settings data, use the default settings and push to firebase
        elif pull_fb and not all_settings:
            # Create a new file, and add in the default settings
            settings = DEFAULT_SETTINGS
            temp = _PATH + ".tmp"
            try:
                with open(temp, "w", encoding="utf-8") as f:
                    json.dump(settings, f, ensure_ascii=False, indent=4)
                os.replace(temp, _PATH)

                user_settings_ref = db.collection("settings").document(curr_user)
                user_settings_ref.update_document(data=settings)
            except:
                return False
            
        # If we are not logged in, just use the default settings
        elif not curr_user:
            try: 
                with open(_PATH, "r", encoding="utf-8") as f:
                    settings = json.load(f)
            except (json.JSONDecodeError, IOError):
                settings = DEFAULT_SETTINGS
            
            settings = DEFAULT_SETTINGS
            ok = _save(None)
            if not ok:
                return False
        
        # If we didnt pull from firebase, then pull from local db
        elif not pull_fb:
            try: 
                with open(_PATH, "r", encoding="utf-8") as f:
                    settings = json.load(f)
            except (json.JSONDecodeError, IOError):
                settings = DEFAULT_SETTINGS

    return dict(settings)

#save to file
def _save(curr_user): 
    try: 
        temp = _PATH + ".tmp" 
        with open(temp, "w", encoding="utf-8") as f:
            json.dump(settings, f, ensure_ascii=False, indent=4)
        os.replace(temp, _PATH)

        if curr_user:
            user_settings_ref = db.collection("settings").document(curr_user)
            user_settings_ref.update_document(data=settings)

        return True #saved successfully
    except IOError:
        return False 

#sets a new setting
def set_setting(setting_id, new_setting, curr_user):
    
    with _lock: 
        settings[setting_id] = new_setting 
        ok = _save(curr_user)

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