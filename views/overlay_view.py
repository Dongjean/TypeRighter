import tkinter as tk
import sys

import utils.shortcuts_unicode as shortcuts_unicode
import utils.unicode_search as unicode_search
import utils.settings as settings

def overlay_init(root):
    border_thickness = 5

    # Reset root for a clean overlay init
    # Remove all child widgets
    for widget in root.winfo_children():
        widget.destroy()
    
    # Initialises root to handle the outline overlay
    root.overrideredirect(True) # No title bar, no borders
    root.attributes("-topmost", True) # Always on top
    root.attributes("-alpha", 0.5) # Translucent, non-intrusive
    if sys.platform.startswith("win"):
        root.state("normal")
        root.attributes("-transparentcolor", "white") # Make anything white in root transparent
    elif sys.platform.startswith("linux"):
        # "#000001" is a funny color which unintentionally renders as near transparent
        # This may not work right now
        root.configure(bg="#000001")
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    root.geometry(f"{sw}x{sh}+0+0")
    if sys.platform.startswith("win"):
        canvas = tk.Canvas(root, bg="white", highlightthickness=0, name="overlay")
    elif sys.platform.startswith("linux"):
        canvas = tk.Canvas(root, bg="#000001", highlightthickness=0, name="overlay")
    else:
        canvas = tk.Canvas(root, bg="white", highlightthickness=0, name="overlay")

    canvas.pack(fill=tk.BOTH, expand=True)
    if sys.platform.startswith("win"):
        canvas.create_rectangle(border_thickness//2, border_thickness//2, sw - border_thickness//2, sh - border_thickness//2, outline="green", width=border_thickness, fill="white", tags="overlay")
    elif sys.platform.startswith("linux"):
        canvas.create_rectangle(border_thickness//2, border_thickness//2, sw - border_thickness//2, sh - border_thickness//2, outline="green", width=border_thickness, fill="", tags="overlay")
    else:
        canvas.create_rectangle(border_thickness//2, border_thickness//2, sw - border_thickness//2, sh - border_thickness//2, outline="green", width=border_thickness, fill="white", tags="overlay")

    # The command textbox
    textbox = tk.Toplevel(root, bg="black", name="textbox") 
    textbox.configure(padx=20, pady=20)
    textbox.transient(root)
    textbox.resizable(False, False)
    textbox.overrideredirect(True) # No title bar, no borders
    textbox.attributes("-topmost", True) # Always on top
    typed = tk.Label(textbox, bg = "black", fg = "white", name="typed")
    typed.pack(pady=5)
    typed.grab_set()
    preview = tk.Label(textbox, bg="black", fg="white", name="preview")
    preview.pack()

    textbox.withdraw()

    # The change template display
    change_template = tk.Toplevel(root, bg="black", name="change_template") 
    change_template.configure(padx=20, pady=20)
    change_template.transient(root)
    change_template.resizable(False, False)
    change_template.overrideredirect(True) # No title bar, no borders
    change_template.attributes("-topmost", True) # Always on top
    curr_template = tk.Label(change_template, text="", bg="black", fg="white", name="curr_template")
    curr_template.pack(pady=5)
    typed.grab_set()
    instructions = tk.Label(change_template, text="Press ESC to exit, arrow keys to change templates", bg="black", fg="white", name="instructions")
    instructions.pack()

    textbox.withdraw()

    # Make sure all of the above tasks of drawing out the overlay view's root window is updated before withdrawing
    # This is because the OS doesnt update anything while the root window is withdrawn
    root.update_idletasks()
    root.withdraw() # Hides the window and canvas first

def trigger_textbox(root):
    toplevel = root.nametowidget("textbox")
    toplevel.lift()
    toplevel.deiconify()

def destroy_textbox(root):
    toplevel = root.nametowidget("textbox")
    prompt = toplevel.nametowidget("typed")
    preview = toplevel.nametowidget("preview")
    preview.configure(text="")
    prompt.configure(text="")
    toplevel.withdraw()

def append_textbox(root, new_keys):
    toplevel = root.nametowidget("textbox")
    prompt = toplevel.nametowidget("typed")
    preview = toplevel.nametowidget("preview")
    curr_symbol = shortcuts_unicode.lookup_unicode(new_keys)
    if curr_symbol:
        preview.configure(text=curr_symbol)
        prompt.configure(text=new_keys, fg="white")
    else:

        unicode_results = unicode_search.search(new_keys)

        if unicode_results:
            preview.configure(text=unicode_results[0][0])
            prompt.configure(text=new_keys, fg="white")
        else:
            preview.configure(text="")
            prompt.configure(text=new_keys, fg="#FF0000")

def trigger_overlay(root):
    global jobId

    # There is a timeout for revert_and_withdraw(), run it upfront now by cancelling the job then calling it
    if jobId:
        root.after_cancel(jobId)
        revert_and_withdraw(root)
    root.deiconify()

def hide_overlay(root):
    root.withdraw()

def revert_and_withdraw(root):
    global jobId
    root.children["overlay"].itemconfig("overlay", outline="green")
    root.update_idletasks() # Allow the canvas to fully paint green first
    hide_overlay(root) # The instant it is back to green, withdraw it
    jobId = None # Job is over

# Global job identifier for revert_and_withdraw()'s timeout function
jobId = None
def flash_red_overlay(root):
    root.children["overlay"].itemconfig("overlay", outline="red")

    global jobId
    jobId = root.after(1000, lambda: revert_and_withdraw(root))

def trigger_change_template(root):
    toplevel = root.nametowidget("change_template")
    curr_template = toplevel.nametowidget("curr_template")

    curr_template_name = settings.lookup_setting("curr_template")
    curr_template.configure(text=curr_template_name)
    toplevel.lift()
    toplevel.deiconify()

def destroy_change_template(root):
    toplevel = root.nametowidget("change_template")
    toplevel.withdraw()

def change_template_display(root, new_template):
    toplevel = root.nametowidget("change_template")
    curr_template = toplevel.nametowidget("curr_template")
    curr_template.configure(text=new_template)