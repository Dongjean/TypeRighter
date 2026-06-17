import pystray
from PIL import Image
from pynput import keyboard
import threading
import os
import sys
import time
import views.view_handler as view_handler
import utils.shortcuts_unicode as shortcuts_unicode
import ctypes

import utils.unicode_search as unicode_search

# For debugging
log_path = os.path.join(os.getcwd(), "debug_log.txt")
sys.stdout = open(log_path, "a", encoding="utf-8", errors="replace", buffering=1) 
sys.stderr = open(log_path, "a", encoding="utf-8", errors="replace", buffering=1)

# Silence terminal for .exe mode
if getattr(sys, 'frozen', False):
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')

# Key listener
keyboard_controller = keyboard.Controller()

# Use canonical keys to account for certain combinations becoming Control Codes
current_keys = set()

def hide_overlay():
    view_handler.gui_queue.put("hide_overlay")

def trigger_overlay():
    view_handler.gui_queue.put("trigger_overlay")

def flash_red_overlay():
    view_handler.gui_queue.put("flash_red_overlay")

def control_panel_window():
    view_handler.gui_queue.put("control_panel_window")

def insert_char(char):

    keyboard_controller.release(BREAKOUT_KEY)
    keyboard_controller.type(char)

keys = ""

def on_press_shortcut(key):
    global keys
    try:
        if hasattr(key, 'char'):
            if key.char != BREAKOUT_KEY:
                keys += key.char
                view_handler.gui_queue.put(f"append_textbox_{keys}")
        elif key == keyboard.Key.backspace:
            keys = keys[:-1]
            view_handler.gui_queue.put(f"append_textbox_{keys}")
        elif key == keyboard.Key.space:
            keys += " "
            view_handler.gui_queue.put(f"append_textbox_{keys}")
    except:
        pass

def on_release_shortcut(key, listener):
    global keys
    try:
        if key.char == BREAKOUT_KEY:
            view_handler.gui_queue.put("destroy_textbox")
            listener.stop()
            if shortcuts_unicode.lookup(keys) == "Close Overlay":
                hide_overlay()
            elif shortcuts_unicode.lookup(keys) == "Control Panel":
                control_panel_window()
            elif shortcuts_unicode.lookup(keys) == "Exit App":
                clean_exit()
            elif unicode_symbol := shortcuts_unicode.copy_symbol(keys):
                threading.Thread(target=lambda: insert_char(unicode_symbol), daemon=True).start()
                overlay_listener = keyboard.Listener(win32_event_filter=lambda msg, data: win32_keyboard_filter(msg, data, overlay_listener))
                overlay_listener.start()
            elif keys == "alpha":
                # Sample, remove this elif in the future
                shortcuts_unicode.copy_to_clipboard("α")
                threading.Thread(target=lambda: insert_char("α"), daemon=True).start()
                overlay_listener = keyboard.Listener(win32_event_filter=lambda msg, data: win32_keyboard_filter(msg, data, overlay_listener))
                overlay_listener.start()
            else:
                # Unicode searching feature
                unicode_results = unicode_search.search(keys, limit=1)

                if unicode_results:
                    # Copy and insert the first unicode result
                    first_result = unicode_results[0][0]
                    shortcuts_unicode.copy_to_clipboard(first_result)
                    threading.Thread(target=lambda: insert_char(first_result), daemon=True).start()
                overlay_listener = keyboard.Listener(win32_event_filter=lambda msg, data: win32_keyboard_filter(msg, data, overlay_listener))
                overlay_listener.start()
            keys = ""
    except:
        pass

# Filter for overlay_listener that filters out BREAKOUT_KEY
def win32_keyboard_filter(msg, data, listener):
    
    # Get the windows virtual key code for BREAKOUT_KEY
    user32 = ctypes.windll.user32
    result = user32.VkKeyScanW(BREAKOUT_KEY)
    breakout_vk_code = result & 0xFF

    # Filter JUST the BREAKOUT_KEY
    if data.vkCode == breakout_vk_code:
        # Once BREAKOUT_KEY is detected, stop overlay_listener
        listener.stop()

        view_handler.gui_queue.put("trigger_textbox")

        # Start shortcut_listener, which catches all keystrokes and runs till BREAKOUT_KEY is released
        shortcut_listener = keyboard.Listener(suppress=True, on_press=lambda key: on_press_shortcut(key), on_release=lambda key: on_release_shortcut(key, shortcut_listener))
        shortcut_listener.start()

        # Dont allow the BREAKOUT_KEY keypress to propagate down
        listener.suppress_event()

def on_press_bg(key, listener):
    if not view_handler.is_control_panel_open:
        canonical_key = listener.canonical(key)
        # If the overlay is on, means we are listening for a 2nd key input
        if canonical_key in map(listener.canonical, COMBINATION):
            current_keys.add(canonical_key)
            if all(k in current_keys for k in map(listener.canonical, COMBINATION)):

                # Release the pressed keys and clear current_keys
                for pressed_key in COMBINATION:
                    keyboard.Controller().release(pressed_key)
                current_keys.clear()

                if not view_handler.is_overlay_triggered:
                    trigger_overlay()
                    # Start a new overlay_listener which listens and catches just "\"
                    overlay_listener = keyboard.Listener(win32_event_filter=lambda msg, data: win32_keyboard_filter(msg, data, overlay_listener))
                    overlay_listener.start()
                elif view_handler.is_overlay_triggered:
                    hide_overlay()
                    stop_all_pynput_keyboard_listeners()
                    bg_listener = keyboard.Listener(on_press=lambda key: on_press_bg(key, bg_listener), on_release=lambda key: on_release_bg(key, bg_listener))
                    bg_listener.start()

def on_release_bg(key, listener):
    canonical_key = listener.canonical(key)
    try:
        current_keys.remove(canonical_key)
    except KeyError:
        pass

# Tray icon
def create_image():
    return Image.new('RGB', (64, 64), (0, 200, 100)) # Green square

def stop_all_pynput_keyboard_listeners():
    # Loop through all active threads in the Python process
    for thread in threading.enumerate():
        # Check if the thread is an instance of a pynput keyboard listener
        if isinstance(thread, (keyboard.Listener)):
            if thread.running:
                thread.stop()

# Clean exit function
def clean_exit():
    print("\nShutting down cleanly...")
    print("___")
    icon.stop() # Stop the tray icon
    stop_all_pynput_keyboard_listeners() # Stop the keyboard listener
    view_handler.gui_queue.put("destroy_root") # Stop the root window
    os._exit(0) # Hard exit to kill all threads instantly

#load saved unicode shortcuts 
shortcuts_unicode.load()
BREAKOUT_KEY = shortcuts_unicode.get_key_from_value("Breakout Key") or "\\"
COMBINATION = [
    keyboard.Key.ctrl_l,
    keyboard.KeyCode.from_char('d'),
]
border_thickness = 5

# Override default Windows behaviour which makes window resolution bad
try:
    # Works on Windows 8.1 and 10+
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    # Fallback for older Windows versions like 7 or XP
    ctypes.windll.user32.SetProcessDPIAware()

if __name__ == "__main__":
    
    # The bg_listener which only listens for the COMBINATION
    bg_listener = keyboard.Listener(on_press=lambda key: on_press_bg(key, bg_listener), on_release=lambda key: on_release_bg(key, bg_listener))
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
    root = view_handler.root_init()
    root.mainloop() # Blocking function