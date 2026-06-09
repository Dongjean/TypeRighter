import tkinter as tk
import queue
import sys

from views.control_panel_view import control_panel_init
from views.overlay_view import trigger_overlay, hide_overlay, flash_red_overlay, overlay_init

# This is the entry point to our GUI window from the main python script

# Thread-safe queue
gui_queue = queue.Queue()

is_overlay_triggered = False
is_control_panel_open = False

# Poll for changes to root window state from other threads
def check_queue(root):
    global is_overlay_triggered
    global is_control_panel_open
    try:
        # Check if there's a message in the queue
        msg = gui_queue.get(block=False)
        if msg == "trigger_overlay":
            trigger_overlay(root)
            is_overlay_triggered = True
        elif msg == "hide_overlay":
            hide_overlay(root)
            is_overlay_triggered = False
        elif msg == "flash_red_overlay":
            flash_red_overlay(root)
            is_overlay_triggered = False
        elif msg == "control_panel_window":
            control_panel_init(root)
            is_overlay_triggered = False
            is_control_panel_open = True
        elif msg == "destroy_root":
            root.destroy()
    except queue.Empty:
        pass

    # Poll every 100 ms
    root.after(100, lambda: check_queue(root))

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

def delete_control_panel_handler(root):
    global is_control_panel_open
    overlay_init(root)
    is_control_panel_open = False