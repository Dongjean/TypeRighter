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
import utils.auth as auth
import utils.settings as settings
import utils.templates as templates

# For debugging
log_path = os.path.join(os.getcwd(), "debug_log.txt")
sys.stdout = open(log_path, "a", encoding="utf-8", errors="replace", buffering=1) 
sys.stderr = open(log_path, "a", encoding="utf-8", errors="replace", buffering=1)

# Key listener
keyboard_controller = keyboard.Controller()

# Use canonical keys to account for certain combinations becoming Control Codes
current_keys = set()

# Update BREAKOUT_KEY when it gets changed in the user flow
def update_breakout_key():
    global BREAKOUT_KEY
    BREAKOUT_KEY = shortcuts_unicode.get_key_from_value("Breakout Key") or "\\"

def hide_overlay():
    view_handler.gui_queue.put("hide_overlay")
    stop_all_pynput_keyboard_listeners()
    bg_listener = keyboard.Listener(on_press=lambda key: on_press_bg(key, bg_listener), on_release=lambda key: on_release_bg(key, bg_listener))
    bg_listener.start()

def trigger_overlay():
    if not view_handler.is_control_panel_open:
        view_handler.gui_queue.put("trigger_overlay")
        # Start a new overlay_listener which listens and catches just "\"
        overlay_listener = keyboard.Listener(win32_event_filter=lambda msg, data: win32_keyboard_filter(msg, data, overlay_listener))
        overlay_listener.start()
    elif view_handler.is_control_panel_open:
        stop_all_pynput_keyboard_listeners()
        view_handler.gui_queue.put("close_control_panel")

def flash_red_overlay():
    view_handler.gui_queue.put("flash_red_overlay")

def control_panel_window():
    view_handler.gui_queue.put("control_panel_window")
    stop_all_pynput_keyboard_listeners()
    bg_listener = keyboard.Listener(on_press=lambda key: on_press_bg(key, bg_listener), on_release=lambda key: on_release_bg(key, bg_listener))
    bg_listener.start()

def trigger_change_template():
    view_handler.gui_queue.put("trigger_change_template")

def destroy_change_template():
    view_handler.gui_queue.put("destroy_change_template")

def insert_char(char):

    keyboard_controller.release(BREAKOUT_KEY)
    keyboard_controller.type(char)

def is_caps_lock_on():
    # Return 1 if Caps Lock is active, 0 if inactive
    return ctypes.windll.user32.GetKeyState(0x14) & 1

keys = ""
is_uppercase = False

def on_press_shortcut(key):
    global keys
    global is_uppercase
    try:
        if hasattr(key, 'char'):
            if key.char != BREAKOUT_KEY:
                if is_uppercase or is_caps_lock_on():
                    keys += key.char.upper()
                else:
                    keys += key.char.lower()
                view_handler.gui_queue.put(f"append_textbox_{keys}")
        elif key == keyboard.Key.backspace:
            keys = keys[:-1]
            view_handler.gui_queue.put(f"append_textbox_{keys}")
        elif key == keyboard.Key.space:
            keys += " "
            view_handler.gui_queue.put(f"append_textbox_{keys}")
        elif key == keyboard.Key.shift:
            is_uppercase = True
    except:
        pass

def on_press_template_change(key, listener):
    try:
        # Exit template change mode
        if key == keyboard.Key.esc or key == keyboard.Key.enter:
            destroy_change_template()
            shortcuts_unicode.load()
            update_breakout_key()
            overlay_listener = keyboard.Listener(win32_event_filter=lambda msg, data: win32_keyboard_filter(msg, data, overlay_listener))
            overlay_listener.start()
            listener.stop()

        # Change keys for selecting templates
        elif key == keyboard.Key.left or key == keyboard.Key.up:
            curr_template_name = settings.lookup_setting("curr_template")
            prev_template_name = templates.get_prev_template_name(curr_template_name)
            templates.use_template(prev_template_name)
            curr_user, e = auth.get_email()
            settings.set_setting("curr_template", prev_template_name, curr_user)
            view_handler.gui_queue.put(f"change_template_display_{prev_template_name}")
        elif key == keyboard.Key.right or key == keyboard.Key.down:
            curr_template_name = settings.lookup_setting("curr_template")
            next_template_name = templates.get_next_template_name(curr_template_name)
            templates.use_template(next_template_name)
            curr_user, e = auth.get_email()
            settings.set_setting("curr_template", next_template_name, curr_user)
            view_handler.gui_queue.put(f"change_template_display_{next_template_name}")
    except:
        pass

def on_release_shortcut(key, listener):
    global keys
    try:
        if hasattr(key, 'char'):
            if key.char == BREAKOUT_KEY:
                view_handler.gui_queue.put("destroy_textbox")
                listener.stop()
                if shortcuts_unicode.lookup_unicode(keys) == "Close Overlay":
                    hide_overlay()
                elif shortcuts_unicode.lookup_unicode(keys) == "Control Panel":
                    control_panel_window()
                elif shortcuts_unicode.lookup_unicode(keys) == "Change Template":
                    if auth.get_email()[0]:
                        trigger_change_template()
                        template_change_listener = keyboard.Listener(suppress=True, on_press=lambda key: on_press_template_change(key, template_change_listener))
                        template_change_listener.start()
                    else:
                        overlay_listener = keyboard.Listener(win32_event_filter=lambda msg, data: win32_keyboard_filter(msg, data, overlay_listener))
                        overlay_listener.start()
                elif shortcuts_unicode.lookup_unicode(keys) == "Exit App":
                    clean_exit()
                elif unicode_symbol := shortcuts_unicode.copy_symbol(keys):
                    threading.Thread(target=lambda: insert_char(unicode_symbol), daemon=True).start()
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
        elif key == keyboard.Key.shift:
            global is_uppercase
            is_uppercase = False
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

        # Release all special keys so no rogue keypress changes occur
        SPECIAL_KEYS = [
            keyboard.Key.shift,
            keyboard.Key.ctrl,
            keyboard.Key.caps_lock,
            keyboard.Key.alt,
            keyboard.Key.tab,
            keyboard.Key.cmd # Windows key
        ]
        for KEY in SPECIAL_KEYS:
            keyboard.Controller().release(KEY)
        
        # Once BREAKOUT_KEY is detected, stop overlay_listener
        listener.stop()

        view_handler.gui_queue.put("trigger_textbox")

        # Start shortcut_listener, which catches all keystrokes and runs till BREAKOUT_KEY is released
        shortcut_listener = keyboard.Listener(suppress=True, on_press=lambda key: on_press_shortcut(key), on_release=lambda key: on_release_shortcut(key, shortcut_listener))
        shortcut_listener.start()

        # Dont allow the BREAKOUT_KEY keypress to propagate down
        listener.suppress_event()

def on_press_bg(key, listener):
    canonical_key = listener.canonical(key)
    # If the overlay is on, means we are listening for a 2nd key input
    if canonical_key in map(listener.canonical, COMBINATION):
        current_keys.add(canonical_key)
        if all(k in current_keys for k in map(listener.canonical, COMBINATION)):
            
            # Release the pressed keys and clear current_keys
            for pressed_key in COMBINATION:
                keyboard.Controller().release(pressed_key)
            current_keys.clear()
            
            if not view_handler.is_control_panel_open:
                if not view_handler.is_overlay_triggered:
                    trigger_overlay()
                elif view_handler.is_overlay_triggered:
                    hide_overlay()
            
            elif view_handler.is_control_panel_open:
                listener.stop()
                view_handler.gui_queue.put("close_control_panel")
    
    if canonical_key == keyboard.Key.shift:
        global is_uppercase
        is_uppercase = True

def on_release_bg(key, listener):
    canonical_key = listener.canonical(key)
    try:
        current_keys.remove(canonical_key)
    except KeyError:
        pass

    if canonical_key == keyboard.Key.shift:
        global is_uppercase
        is_uppercase = False

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
    try:
        view_handler.icon.stop() # Stop the tray icon
        stop_all_pynput_keyboard_listeners() # Stop the keyboard listener
        view_handler.gui_queue.put("destroy_root") # Stop the root window
    except Exception as e:
        print(e)
    finally:
        os._exit(0) # Hard exit to kill all threads instantly

# Login, if its still valid
email, e = auth.get_email()
if email:
    print(f"logged in as: {email}")
    # Load the settings
    curr_settings = settings.load(email, pull_fb=True)

    # Load the current template
    templates.load(email, pull_fb=False)
    templates.use_template(curr_settings["curr_template"])
else:
    print(f"error initialising login state: {e}")

# Load saved unicode shortcuts
# If logged in properly, the saved one will be loaded
# If not logged in, the default shortcuts will be loaded
shortcuts_unicode.load()

BREAKOUT_KEY = shortcuts_unicode.get_key_from_value("Breakout Key") or "\\"
COMBINATION = [
    keyboard.Key.ctrl_l,
    keyboard.Key.alt_l,
    keyboard.Key.space
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
        pystray.MenuItem("Open Control Panel", lambda icon, item: control_panel_window()),
        pystray.MenuItem("Trigger Overlay", lambda icon, item: trigger_overlay()),
        pystray.MenuItem("Close Overlay", lambda icon, item: hide_overlay()),
        pystray.MenuItem("Exit", lambda icon, item: clean_exit())
    )
    # .run_detached() starts a non-blocking non-daemon thread
    icon.run_detached()

    # Save a reference to icon attached to view_handler so it can be accessed from other threads
    view_handler.icon = icon

    # Initialise and run main_view.root
    root = view_handler.root_init()
    root.mainloop() # Blocking function