import tkinter as tk
import queue

# Thread-safe queue
gui_queue = queue.Queue()

# Opening up the global root for the tkinter
root = tk.Tk()

# Poll for changes to root window state from other threads
def check_queue():
  try:
    # Check if there's a message in the queue
    msg = gui_queue.get(block=False)
    print(msg)
    if msg == "trigger_overlay":
      trigger_overlay()
    elif msg == "hide_overlay":
      hide_overlay()
    elif msg == "flash_red_overlay":
      flash_red_overlay()
  except queue.Empty:
    pass

  # Poll every 100 ms
  root.after(100, check_queue)

def window():
  root = tk.Tk()
  root.title("TypeRighter")
  root.geometry("400x300")

  label = tk.Label(root, text="Hello!")
  label.pack()

  button = tk.Button(root, text="Click me")
  button.pack()
  root.mainloop()

overlay_root = None
def root_init():
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

  # Run check_queue() the moment the root window opens
  root.after(0, lambda: check_queue())
  root.mainloop() # Blocking function

def trigger_overlay():
  global jobId

  # There is a timeout for revert_and_withdraw(), run it upfront now by cancelling the job then calling it
  if jobId:
    root.after_cancel(jobId)
    revert_and_withdraw()
  root.deiconify()

def hide_overlay():
  root.withdraw()

def revert_and_withdraw():
  global jobId
  root.children["overlay"].itemconfig("overlay", outline="green")
  root.update_idletasks() # Allow the canvas to fully paint green first
  hide_overlay() # The instant it is back to green, withdraw it
  jobId = None # Job is over

# Global job identifier for revert_and_withdraw()'s timeout function
jobId = None
def flash_red_overlay():
  root.children["overlay"].itemconfig("overlay", outline="red")

  global jobId
  jobId = root.after(1000, lambda: revert_and_withdraw())

def overlay_box():
  border_thickness = 5

  root = tk.Tk()

  root.overrideredirect(True) # No title bar, no borders
  root.attributes("-topmost", True) # Always on top
  root.attributes("-alpha", 0.5) # Translucent, non-intrusive
  root.attributes("-transparentcolor", "white") # Make anything white in root transparent
  sw = root.winfo_screenwidth()
  sh = root.winfo_screenheight()
  root.geometry(f"{sw}x{sh}+0+0")

  # Draw border box using canvas
  # White was set as transparent
  canvas = tk.Canvas(root, bg="white", highlightthickness=0)
  canvas.pack(fill=tk.BOTH, expand=True)
  canvas.create_rectangle(border_thickness//2, border_thickness//2, sw - border_thickness//2, sh - border_thickness//2, outline="green", width=border_thickness, fill="white")

  # So we can call main_view.overlay_root.destroy() later
  global overlay_root
  overlay_root = root
  
  root.mainloop() # Blocking function

  # Clear overlay_root after we are done
  overlay_root = None