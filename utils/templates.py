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
def _save(curr_user, template_name, new_template):
    try:
        if template_name and curr_user:
            _TEMPLATE_PATH = os.path.join(_templates_dir(curr_user), "user_templates.json")
            temp = _TEMPLATE_PATH + ".tmp"

            # Read the existing file and change our current new_template
            with open(_TEMPLATE_PATH, "r", encoding="utf-8") as f:
                try:
                    all_templates = json.load(f)
                    all_templates[template_name] = new_template
                except Exception as e:
                    print(e)
                    return False

            # Replace the old file with the new template objects
            with open(temp, "w", encoding="utf-8") as f:
                json.dump(all_templates, f, ensure_ascii=False, indent=4)
            os.replace(temp, _TEMPLATE_PATH)
        return True
    except IOError:
        return False

# Updates a template
def update_template(curr_user, template_name, new_template):
    
    ok = _save(curr_user, template_name, new_template)

    if ok: 
        return True, f"Successfully set '{template_name}' to '{new_template}' for user '{curr_user}'."
    else: 
        return False, f"Failed to set '{template_name}' to '{new_template}' for user '{curr_user}. Please try again."

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

# def new_template(curr_user, template_name, template):
#     global templates

#     _CURR_TEMPLATES_PATH = os.path.join(_templates_dir(curr_user), "user_template.json")
#     with _lock:
#         try:
