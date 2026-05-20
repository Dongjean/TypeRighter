import pystray
from PIL import Image
from pynput import keyboard
import threading
import os
import sys
import time
import views.main_view as main_view
import queue

# Thread-safe queue
indicator_queue = queue.Queue()

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
    # Queue the display of the indicator
    # This is pushed from the keyboard listener thread
    # This will be picked up by the main thread in the main loop
    if indicator_queue.qsize() == 0:
        indicator_queue.put("SHOW_INDICATOR")


# Key listener

# Use canonical keys to account for certain combinations becoming Control Codes
current_keys = set()
def on_press(key):
    print(main_view.overlay_root)
    # If the overlay is on, means we are listening for a 2nd key input
    if main_view.overlay_root:

        # Close the overlay
        if key == keyboard.KeyCode.from_char('a'):
            main_view.overlay_root.after(0, main_view.overlay_root.destroy)
            return
    canonical_key = listener.canonical(key)
    if canonical_key in COMBINATION:
        current_keys.add(canonical_key)
        if all(k in current_keys for k in COMBINATION):
            # Run the window in its own thread so it doesn't freeze the listener
            # Overlay runs on tkinter, which doesnt work well with threads
            # Queue it to run it on the main thread for stability
            trigger_window()

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

            # Poll the queue to see if we are to show the indicator
            try:
                indicator_status = indicator_queue.get(block=False)
                if indicator_status == "SHOW_INDICATOR":
                    # Add a status check so that the keyboard listener's thread's on_press() doesnt queue another "SHOW_INDICATOR"
                    indicator_queue.put("SHOWING")
                    print("the indicator is listening, and now blocking the main thread")
                    main_view.overlay_box() # Blocking Function running on main thread (stable for tkinter)
                    indicator_queue.get() # Remove the "SHOWING" status from queue to reset the system
            except:
                pass
    except KeyboardInterrupt:
        print("Script terminated via Ctrl+C")
        clean_exit()