import tkinter as tk
import queue
import sys
from pynput import keyboard
from urllib.parse import urlparse, parse_qs

from views.control_panel_view import control_panel_init
from views.overlay_view import trigger_overlay, hide_overlay, flash_red_overlay, overlay_init, trigger_textbox, destroy_textbox, append_textbox, trigger_change_template, destroy_change_template, change_template_display
import __main__ as main

# This is the entry point to our GUI window from the main python script

# Thread-safe queue
gui_queue = queue.Queue()

is_overlay_triggered = False
is_control_panel_open = False
is_changing_template = False

# Poll for changes to root window state from other threads
def check_queue(root):
    global is_overlay_triggered
    global is_control_panel_open
    global is_changing_template
    try:
        # Check if there's a message in the queue
        msg = gui_queue.get(block=False)

        # Trigger the Overlay
        if msg == "trigger_overlay":
            trigger_overlay(root)
            is_overlay_triggered = True
        
        # Hide the Overlay
        elif msg == "hide_overlay":
            hide_overlay(root)
            is_overlay_triggered = False

        # Flash the Overlay Red (unused currently)
        elif msg == "flash_red_overlay":
            flash_red_overlay(root)
            is_overlay_triggered = False
        
        # Open the Control Panel
        elif msg == "control_panel_window":
            control_panel_init(root)
            is_overlay_triggered = False
            is_control_panel_open = True
        
        # Template Changing Commands
        elif msg == "trigger_change_template":
            trigger_change_template(root)
        elif msg == "destroy_change_template":
            destroy_change_template(root)
        elif msg.startswith("change_template_display_"):
            change_template_display(root, msg.removeprefix("change_template_display_"))
        
        # Command Textbox Commands
        elif msg == "trigger_textbox":
            trigger_textbox(root)
        elif msg == "destroy_textbox":
            destroy_textbox(root)
        elif msg.startswith("append_textbox_"):
            append_textbox(root, msg.removeprefix("append_textbox_"))

        # For returning back to Overlay Mode or BG Listener Mode from CP-Mode with COMBINATION
        elif msg.startswith("close_control_panel"):
            entry_point = msg.removeprefix("close_control_panel/entry=")
            print(entry_point)
            if entry_point == "bg_listener_mode":
                delete_control_panel_handler(root, entry=entry_point)
            else:
                delete_control_panel_handler(root, entry="overlay_mode")
        
        # For Exiting the App
        elif msg == "destroy_root":
            root.destroy()
    except queue.Empty:
        pass

    # Poll every 10 ms
    root.after(10, lambda: check_queue(root))

def root_init():

    root = tk.Tk()

    # We are starting the app with overlay, initialize the root window with it
    overlay_init(root)

    # Run check_queue() the moment the root window opens
    root.after(0, lambda: check_queue(root))

    # Run delete_control_panel_handler() when the root window is closed
    # If we are in the control panel, we are back to overlay mode
    # If we are in overlay mode and somehow reach this, we still stay in overlay mode
    # Defining this callback function for WM_DELETE_WINDOW overrides the default behaviour, so it wont run root.destroy()
    root.protocol("WM_DELETE_WINDOW", lambda: delete_control_panel_handler(root))
    return root

def delete_control_panel_handler(root, entry="overlay_mode"):
    global is_control_panel_open, is_overlay_triggered

    # Close the Control Panel and switch on the Overlay
    overlay_init(root)
    is_control_panel_open = False

    if entry == "overlay_mode":
        is_overlay_triggered = True
        trigger_overlay(root)
        # Start a new overlay_listener which listens and catches just "\"
        # Start this only if the we are entering Overlay Mode
        overlay_listener = keyboard.Listener(win32_event_filter=lambda msg, data: main.win32_keyboard_filter(msg, data, overlay_listener))
        overlay_listener.start()
    elif entry == "bg_listener_mode":
        is_overlay_triggered = False

    # Starts a new bg_listener to listen for COMBINATION too
    bg_listener = keyboard.Listener(on_press=lambda key: main.on_press_bg(key, bg_listener), on_release=lambda key: main.on_release_bg(key, bg_listener))
    bg_listener.start()