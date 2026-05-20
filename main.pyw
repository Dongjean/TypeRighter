import pystray
from PIL import Image
from pynput import keyboard
import threading
import os
import sys
import time
import views.main_view as main_view

# For debugging
log_path = os.path.join(os.getcwd(), "debug_log.txt")
sys.stdout = open(log_path, "a", buffering=1) 
sys.stderr = open(log_path, "a", buffering=1)

# Silence terminal for .exe mode
if getattr(sys, 'frozen', False):
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')

def trigger_overlay():
    global is_overlay_triggered
    main_view.root.event_generate("<<trigger_overlay>>", when="tail")
    is_overlay_triggered = True

def hide_overlay():
    global is_overlay_triggered
    main_view.root.event_generate("<<hide_overlay>>", when="tail")
    is_overlay_triggered = False

# Key listener

# Use canonical keys to account for certain combinations becoming Control Codes
is_overlay_triggered = False
current_keys = set()
def on_press(key):
    canonical_key = listener.canonical(key)
    # If the overlay is on, means we are listening for a 2nd key input
    if is_overlay_triggered:

        # Close the overlay
        if key == keyboard.KeyCode.from_char('a'):
            hide_overlay()
            return
    elif canonical_key in COMBINATION:
        current_keys.add(canonical_key)
        if all(k in current_keys for k in COMBINATION):
            trigger_overlay()

def on_release(key):
    canonical_key = listener.canonical(key)
    try:
        current_keys.remove(canonical_key)
    except KeyError:
        pass

# Tray icon
def create_image():
    return Image.new('RGB', (64, 64), (0, 200, 100)) # Green square

# Clean exit function
def clean_exit():
    print("\nShutting down cleanly...")
    print("___")
    icon.stop() # Stop the tray icon
    listener.stop() # Stop the keyboard listener
    os._exit(0) # Hard exit to kill all threads instantly

border_thickness = 5
if __name__ == "__main__":
    # Start Listener
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    COMBINATION = {
        listener.canonical(keyboard.Key.ctrl_l),
        keyboard.KeyCode.from_char('d'),
    }
    # .start() starts a non-blocking daemon thread
    listener.start()

    # Start Tray Icon
    icon = pystray.Icon("TypeRighter")
    icon.icon = create_image()
    icon.menu = pystray.Menu(
        pystray.MenuItem("Run Now", lambda icon, item: trigger_overlay()),
        pystray.MenuItem("Exit", lambda icon, item: clean_exit())
    )
    # .run_detached() starts a non-blocking non-daemon thread
    icon.run_detached()

    # Initialise and run main_view.root
    main_view.root_init() # Blocking function