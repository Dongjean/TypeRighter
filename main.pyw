import pystray
from PIL import Image
from pynput import keyboard
import threading
import os
import sys
import time
from views.main_view import overlay_box

# For debuggin
log_path = os.path.join(os.getcwd(), "debug_log.txt")
sys.stdout = open(log_path, "a", buffering=1) 
sys.stderr = open(log_path, "a", buffering=1)

# Silence terminal for .exe mode
if getattr(sys, 'frozen', False):
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')

# The trigger action
def trigger_window():
    overlay_box()

# Key listener

# Use canonical keys to account for certain combinations becoming Control Codes
current_keys = set()
def on_press(key):
    canonical_key = listener.canonical(key)
    if canonical_key in COMBINATION:
        current_keys.add(canonical_key)
        if all(k in current_keys for k in COMBINATION):
            # Run the window in its own thread so it doesn't freeze the listener
            threading.Thread(target=trigger_window, daemon=True).start()

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
        pystray.MenuItem("Run Now", trigger_window),
        pystray.MenuItem("Exit", lambda icon, item: clean_exit())
    )
    # .run_detached() starts a non-blocking non-daemon thread
    icon.run_detached()

    # Listen for CTRL+C to exit when testing in terminal
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Script terminated via Ctrl+C")
        clean_exit()