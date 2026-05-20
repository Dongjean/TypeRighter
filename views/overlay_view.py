import tkinter as tk

def overlay_init(root):
    border_thickness = 5
    # Initialises root to handle the outline overlay
    root.overrideredirect(True) # No title bar, no borders
    root.attributes("-topmost", True) # Always on top
    root.attributes("-alpha", 0.5) # Translucent, non-intrusive
    root.attributes("-transparentcolor", "white") # Make anything white in root transparent
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    root.geometry(f"{sw}x{sh}+0+0")
    canvas = tk.Canvas(root, bg="white", highlightthickness=0, name="overlay")
    canvas.pack(fill=tk.BOTH, expand=True)
    canvas.create_rectangle(border_thickness//2, border_thickness//2, sw - border_thickness//2, sh - border_thickness//2, outline="green", width=border_thickness, fill="white", tags="overlay")
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
