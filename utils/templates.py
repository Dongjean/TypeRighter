import json 
import os 
import sys 
import threading 
import shutil

import utils.firebase_app as fb
import utils.settings as settings

db = fb.db

def _data_dir(): 
    app = "TypeRighter"
    if sys.platform !="win32":
        raise NotImplementedError("This function is currently only implemented for Windows.")
    
    base = os.environ.get("APPDATA", os.path.expanduser("~"))
    folder = os.path.join(base, app)
    os.makedirs(folder, exist_ok=True)
    return folder

#creates local file (windows)
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

def _user_dir(curr_user): 
    app = "TypeRighter"
    user_folder = curr_user
    if sys.platform !="win32":
        raise NotImplementedError("This function is currently only implemented for Windows.")
    
    base = os.environ.get("APPDATA", os.path.expanduser("~"))
    folder = os.path.join(base, app, user_folder)
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

_lock = threading.Lock()

templates = {
    "default": DEFAULT_BINDINGS
}

#load the templates for the current user.
def load(curr_user, pull_fb=False):
    global templates
    # Get the path for the current user
    _PATH = os.path.join(_templates_dir(curr_user), "user_templates.json")

    # Pull the templates data from firebase if required
    if pull_fb:
        try:
            user_templates_ref = db.collection("templates")
            all_templates = user_templates_ref.get_document(curr_user)
        except:
            pass

    with _lock:

        # If we successfully pulled templates data from firebase, write to file
        if pull_fb and all_templates:
            templates = all_templates
            temp = _PATH + ".tmp"
            try:
                with open(temp, "w", encoding="utf-8") as f:
                    json.dump(all_templates, f, ensure_ascii=False, indent=4)
                os.replace(temp, _PATH)
            except:
                return False
        
        # If firebase has no valid templates data, use the default templates
        elif pull_fb and not all_templates:
            # Create a new default templates file and add in the default template
            templates = {
                "default": DEFAULT_BINDINGS
            }
            temp = _PATH + ".tmp"
            try:
                with open(temp, "w", encoding="utf-8") as f:
                    json.dump(templates, f, ensure_ascii=False, indent=4)
                os.replace(temp, _PATH)

                user_templates_ref = db.collection("templates").document(curr_user)
                user_templates_ref.update_document(data=templates)
            except:
                return False
        
        # If we didnt pull from firebase, then pull from local db
        elif not pull_fb:
            try:
                with open(_PATH, "r", encoding="utf-8") as f:
                    templates = json.load(f)
            except (json.JSONDecodeError, IOError):
                templates = { "default": {} }

#save to file
def _save(curr_user):
    try:
        if curr_user:
            _TEMPLATE_PATH = os.path.join(_templates_dir(curr_user), "user_templates.json")
            temp = _TEMPLATE_PATH + ".tmp"

            # Replace the old file with the new template objects
            with open(temp, "w", encoding="utf-8") as f:
                json.dump(templates, f, ensure_ascii=False, indent=4)
            os.replace(temp, _TEMPLATE_PATH)

        # Add a template_names list so we can dynamically call all the templates later
        user_templates_ref = db.collection("templates").document(curr_user)
        user_templates_ref.create_document(data=templates)

        return True
    except IOError:
        return False

def _delete_templates_folder(curr_user):
    try:
        _USER_DIR = _user_dir(curr_user)
        shutil.rmtree(_USER_DIR)
    except:
        return False

# Updates a template
def update_template(curr_user, template_name, new_template):
    global templates

    with _lock:
        templates[template_name] = new_template
        ok = _save(curr_user)

    if ok:
        return True, f"Successfully set '{template_name}' to '{new_template}' for user '{curr_user}'."
    else: 
        return False, f"Failed to set '{template_name}' to '{new_template}' for user '{curr_user}. Please try again."

def rename_template(curr_user, old_template_name, new_template_name):
    global templates

    with _lock:
        template = templates.pop(old_template_name)
        templates[new_template_name] = template

        ok = _save(curr_user)

    if ok:
        return True, f"Successfully Renamed Template '{old_template_name}' to '{new_template_name}' for user '{curr_user}'."
    else: 
        return False, f"Failed to Rename Template '{old_template_name}' to '{new_template_name}' for user '{curr_user}. Please try again."

def delete_template(curr_user, template_name):
    global templates

    with _lock:
        templates.pop(template_name)

        ok = _save(curr_user)

    if ok:
        return True, f"Successfully Deleted Template '{template_name}' for user '{curr_user}'."
    else: 
        return False, f"Failed to Delete Template '{template_name}' for user '{curr_user}. Please try again."

#shows all templates
def all_templates(curr_user):
    global templates

    if templates:
        return dict(templates)
    else:
        _PATH = _templates_dir(curr_user)

        _TEMPLATES_PATH = os.path.join(_PATH, "user_templates.json")

        if os.path.exists(_TEMPLATES_PATH):
            try:
                with open(_TEMPLATES_PATH, "r", encoding="utf-8") as f:
                    curr_template = json.load(f)
                    templates = curr_template
            except (json.JSONDecodeError, IOError):
                pass
        
        return dict(templates)

def use_template(template_name):

    _SELECTED_TEMPLATE_PATH = os.path.join(_data_dir(), "shortcuts.json")

    selected_template = templates.get(template_name)

    if not selected_template:
        return False

    with _lock:
        try:
            temp = _SELECTED_TEMPLATE_PATH + ".tmp" 
            with open(temp, "w", encoding="utf-8") as f:
                json.dump(selected_template, f, ensure_ascii=False, indent=4)
            os.replace(temp, _SELECTED_TEMPLATE_PATH)
            return True
        except IOError:
            return False

def get_prev_template_name(curr_template):

    with _lock:
        try:
            templates_keys = list(templates.keys())
        except:
            return False
    
    current_index = templates_keys.index(curr_template)

    prev_index = (current_index - 1) % len(templates_keys)

    return templates_keys[prev_index]
    
def get_next_template_name(curr_template):

    with _lock:
        try:
            templates_keys = list(templates.keys())
        except:
            return False
    
    current_index = templates_keys.index(curr_template)

    next_index = (current_index + 1) % len(templates_keys)

    return templates_keys[next_index]

def delete_user_data(curr_user):    
    global templates

    templates = {"default": DEFAULT_BINDINGS}

    ok = _delete_templates_folder(curr_user)

    if ok:
        return True
    else:
        return False

# def new_template(curr_user, template_name, template):
#     global templates

#     _CURR_TEMPLATES_PATH = os.path.join(_templates_dir(curr_user), "user_template.json")
#     with _lock:
#         try:

BASE_TEMPLATE_NAME = "New_Template"
def add_new_template(email):
    global templates

    with _lock:
        template_names = list(templates)

        if BASE_TEMPLATE_NAME not in template_names:
            new_template_name = BASE_TEMPLATE_NAME
            templates[new_template_name] = DEFAULT_BINDINGS

            ok = _save(email)

        else:
            counter = 1
            new_template_name = BASE_TEMPLATE_NAME + "_" + str(counter)
            while new_template_name in template_names:
                counter += 1
                new_template_name = new_template_name[:-1] + str(counter)

            templates[new_template_name] = DEFAULT_BINDINGS

            ok = _save(email)
    
    if ok:
        return new_template_name
    else:
        return False