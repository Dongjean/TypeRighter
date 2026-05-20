import tkinter as tk

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