import tkinter as tk
import sys

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
    # Make sure all of the above tasks of drawing out the overlay view's root window is updated before withdrawing
    # This is because the OS doesnt update anything while the root window is withdrawn
    root.update_idletasks()
    root.withdraw() # Hides the window and canvas first

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
