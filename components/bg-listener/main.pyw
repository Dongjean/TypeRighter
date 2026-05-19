# import pystray
# from PIL import Image
# from pynput import keyboard
# from plyer import notification # New library for popups
# import threading
# import os

# import sys
# import os
# log_path = os.path.join(os.getcwd(), "debug_log.txt")
# sys.stdout = open(log_path, "a", buffering=1) 
# sys.stderr = open(log_path, "a", buffering=1)

# # --- 1. THE ACTION WITH POPUP ---
# def trigger_popup():
#     notification.notify(
#         title="Command Received",
#         message="I'm running your custom script now! 🚀",
#         app_name="My Background Listener",
#         # app_icon="icon.ico", # Optional: link to a .ico file for a custom look
#         timeout=3 # How many seconds the popup stays visible
#     )
#     print("Notification sent!")

# # --- 2. THE LISTENER ---
# def start_global_listener():
#     with keyboard.GlobalHotKeys({
#             '<ctrl>+<space>': trigger_popup
#         }) as h:
#         h.join()

# # --- 3. THE TRAY ICON ---
# def create_image():
#     # Simple 64x64 blue square for the tray
#     image = Image.new('RGB', (64, 64), (0, 120, 215))
#     return image

# def on_quit(icon, item):
#     icon.stop()
#     os._exit(0)

# # --- 4. EXECUTION ---
# if __name__ == "__main__":
#     # Start the listener thread
#     threading.Thread(target=start_global_listener, daemon=True).start()

#     # Setup the Tray Icon
#     icon = pystray.Icon("GlobalCommandCenter")
#     icon.menu = pystray.Menu(
#         pystray.MenuItem("Trigger Test", trigger_popup),
#         pystray.MenuItem("Exit", on_quit)
#     )
#     icon.icon = create_image()
#     icon.title = "Always Listening..."

#     icon.run()

import pystray
from PIL import Image
from pynput import keyboard
import threading
import os
import sys
import tkinter as tk
from tkinter import messagebox

log_path = os.path.join(os.getcwd(), "debug_log.txt")
sys.stdout = open(log_path, "a", buffering=1) 
sys.stderr = open(log_path, "a", buffering=1)

# Silence terminal for .exe mode
if getattr(sys, 'frozen', False):
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')

# --- 1. THE ACTION (WINDOW) ---
def trigger_window():
    # We create a temporary hidden window so the messagebox has a parent
    root = tk.Tk()
    root.withdraw()  # Hide the main tiny Tkinter window
    root.attributes("-topmost", True) # Force it to the front
    
    # This creates the actual "Window" popup
    messagebox.showinfo("Command Center", "Command Executed Successfully!")
    
    root.destroy() # Clean up memory after you click 'OK'

# --- 2. THE LISTENER (Manual Combo for Stability) ---
current_keys = set()
COMBINATION = {
    keyboard.Key.ctrl_l, 
    keyboard.Key.space
}

def on_press(key):
    if key in COMBINATION:
        current_keys.add(key)
        if all(k in current_keys for k in COMBINATION):
            # Run the window in its own thread so it doesn't freeze the listener
            threading.Thread(target=trigger_window, daemon=True).start()

def on_release(key):
    try:
        current_keys.remove(key)
    except KeyError:
        pass

# --- 3. THE TRAY ICON & EXECUTION ---
def create_image():
    return Image.new('RGB', (64, 64), (0, 200, 100)) # Green icon

if __name__ == "__main__":
    # Start Listener
    threading.Thread(target=lambda: keyboard.Listener(on_press=on_press, on_release=on_release).start(), daemon=True).start()

    # Start Tray Icon
    icon = pystray.Icon("WindowApp")
    icon.icon = create_image()
    icon.menu = pystray.Menu(
        pystray.MenuItem("Run Now", trigger_window),
        pystray.MenuItem("Exit", lambda: os._exit(0))
    )
    icon.run()