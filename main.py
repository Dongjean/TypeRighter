import pystray
from PIL import Image
from pynput import keyboard
import threading
import os
import sys
import time
import views.root_view as root_view
import utils.shortcuts_unicode as shortcuts_unicode

# For debugging
log_path = os.path.join(os.getcwd(), "debug_log.txt")
sys.stdout = open(log_path, "a", encoding="utf-8", errors="replace", buffering=1) 
sys.stderr = open(log_path, "a", encoding="utf-8", errors="replace", buffering=1)

# Silence terminal for .exe mode
if getattr(sys, 'frozen', False):
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')

# Key listener

# Use canonical keys to account for certain combinations becoming Control Codes
current_keys = set()

def hide_overlay():
    root_view.gui_queue.put("hide_overlay")

def trigger_overlay():
    root_view.gui_queue.put("trigger_overlay")

def flash_red_overlay():
    root_view.gui_queue.put("flash_red_overlay")

def control_panel_window():
    root_view.gui_queue.put("control_panel_window")

def on_press_shortcut(key, listener):

    # The overlay is on, so we are listening for a 2nd key input
    if root_view.is_overlay_triggered:
        try: 
            key_char = key.char
            
        except AttributeError:
            key_char = None 
            
        # Close the overlay
        if key == keyboard.KeyCode.from_char('a'):
            hide_overlay()
        
        # Control panel window
        elif key == keyboard.KeyCode.from_char('\\'):
            control_panel_window()
        
        #Unicode Shortcut 
        elif key_char and shortcuts_unicode.copy_symbol(key_char):
            hide_overlay()

        # FOR DEBUG EASE
        elif key == keyboard.KeyCode.from_char('`'):
            clean_exit()

        # No recognised key
        else:
            flash_red_overlay()
    
    # After a single press event, return back to bg_listener

    # Stop shortcut_listener
    listener.stop()

    # Start a new bg_listener
    bg_listener = keyboard.Listener(on_press=lambda key: on_press_bg(key, bg_listener), on_release=lambda key: on_release_bg(key, bg_listener))
    global COMBINATION
    COMBINATION = {
        bg_listener.canonical(keyboard.Key.ctrl_l),
        keyboard.KeyCode.from_char('d'),
    }
    bg_listener.start()

def on_press_bg(key, listener):
    if not root_view.is_control_panel_open:
        canonical_key = listener.canonical(key)
        # If the overlay is on, means we are listening for a 2nd key input

        if canonical_key in COMBINATION:
            current_keys.add(canonical_key)
            if all(k in current_keys for k in COMBINATION):
                trigger_overlay()

                # Before we stop bg_listener, release the pressed keys and clear current_keys
                for pressed_key in COMBINATION:
                    keyboard.Controller().release(pressed_key)
                current_keys.clear()
                # Stop the bg_listener
                listener.stop()

                # Start a new shortcut_listener which suppresses typing
                shortcut_listener = keyboard.Listener(suppress=True, on_press=lambda key: on_press_shortcut(key, shortcut_listener))
                shortcut_listener.start()

def on_release_bg(key, listener):
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
    # listener.stop() # Stop the keyboard listener
    # Loop through all active threads in the Python process
    for thread in threading.enumerate():
        # Check if the thread is an instance of a pynput keyboard listener
        if isinstance(thread, (keyboard.Listener)):
            if thread.running:
                thread.stop()
    root_view.gui_queue.put("destroy_root") # Stop the root window
    os._exit(0) # Hard exit to kill all threads instantly

#load saved unicode shortcuts 
shortcuts_unicode.load()
COMBINATION = {}
border_thickness = 5
if __name__ == "__main__":
    
    # The bg_listener which only listens for the COMBINATION
    bg_listener = keyboard.Listener(on_press=lambda key: on_press_bg(key, bg_listener), on_release=lambda key: on_release_bg(key, bg_listener))
    COMBINATION = {
        bg_listener.canonical(keyboard.Key.ctrl_l),
        keyboard.KeyCode.from_char('d'),
    }
    # Start Listener
    # .start() starts a non-blocking daemon thread
    bg_listener.start()

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
    root = root_view.root_init()
    root.mainloop() # Blocking function