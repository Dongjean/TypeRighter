import json 
import os 
import sys 
import threading 
import shutil

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

DEFAULT_BINDINGS = {
    "unicode": {
        "`": "Exit App",
        "a": "Close Overlay",
        "s": "Control Panel",
        "\\": "Breakout Key",
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
def load(curr_user):
    global templates
    # Get the path for the current user
    _PATH = os.path.join(_templates_dir(curr_user), "user_templates.json")
    with _lock:
        # Create the new folder for this user's templates if it doesnt already exist
        # Otherwise read it
        if os.path.exists(_PATH):
            try:
                with open(_PATH, "r", encoding="utf-8") as f:
                    templates = json.load(f)
            except (json.JSONDecodeError, IOError):
                templates = { "default": {} }
        if not os.path.exists(_PATH):
            # Create a new default templates file and add in the default template
            templates = {
                "default": DEFAULT_BINDINGS
            }
            temp = _PATH + ".tmp"
            with open(temp, "w", encoding="utf-8") as f:
                json.dump(templates, f, ensure_ascii=False, indent=4)
            os.replace(temp, _PATH)

#save to file
def _save(curr_user, template_id, new_template):
    try:

        template_number_int = int(template_id.split("_")[1])
        base_dir = _templates_dir(curr_user)

        # First find if this template_id already exists, and if it doesnt, find the next available number
        is_new = True
        counter = 1
        while True and is_new:
            filename = f"template_{counter}.json"
            _PATH = os.path.join(base_dir, filename)
            
            # If template_no already exists, then update this template
            if os.path.exists(_PATH) and (template_number_int == counter):
                is_new = False
                break

            # If this specific template doesn't exist, we can use f"template_{counter}.json"
            if not os.path.exists(_PATH):
                break

            counter += 1
        
        template_filename = f"template_{counter}.json"
        
        _PATH = os.path.join(_templates_dir(curr_user), template_filename)
        temp = _PATH + ".tmp" 
        with open(temp, "w", encoding="utf-8") as f:
            json.dump(new_template, f, ensure_ascii=False, indent=4)
        os.replace(temp, _PATH)
        return True #saved successfully
    except IOError:
        return False 

#sets or updates a template
def set_template(curr_user, template_id, new_template):
    
    ok = _save(curr_user, template_id, new_template)

    if ok: 
        return True, f"Successfully set '{template_id}' to '{new_template}' for user '{curr_user}'."
    else: 
        return False, f"Failed to set '{template_id}' to '{new_template}' for user '{curr_user}. Please try again."

#shows all templates
def all_templates(curr_user):
    
    templates = {}
    _PATH = _templates_dir(curr_user)

    for template_filename in os.listdir(_PATH):
        curr_path = os.path.join(_PATH, template_filename)

        if os.path.exists(curr_path):
            try:
                with open(curr_path, "r", encoding="utf-8") as f:
                    curr_template = json.load(f)
                    templates[template_filename] = curr_template
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