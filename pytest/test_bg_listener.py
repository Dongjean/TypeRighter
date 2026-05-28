import pytest

# Import main.pyw
# .pyw extension complicates things
import importlib.util
import sys
from pathlib import Path

main_file_path = Path(__file__).parent / "../main.pyw"
main_dir = str(main_file_path.parent)

# Inject this directory to the front of Python's search path
if main_dir not in sys.path:
    sys.path.insert(0, main_dir)

spec = importlib.util.spec_from_file_location("main", main_file_path)
main = importlib.util.module_from_spec(spec)
sys.modules["main"] = main
spec.loader.exec_module(main)
# Now main is can be used like a regular import
import time
from pynput import keyboard

# Manually initialize the tkinter window without .mainloop()
# Run root_view.root_init() without the last root.mainloop() line
root = main.root_view.root
main.root_view.overlay_init(root)
root.after(0, lambda: main.root_view.check_queue())
root.update()

# Start the pynput thread
main.listener.start()

sw = root.winfo_screenwidth()
sh = root.winfo_screenheight()
border_thickness = 5
key_simulator = keyboard.Controller()

def get_overlay_init_tests():

    # All of these should be True
    is_root = root != None
    is_overrideredirect = root.overrideredirect() == True
    is_topmost = root.attributes("-topmost") == True
    is_alpha = root.attributes("-alpha") == 0.5
    is_transparentcolor = str(root.attributes("-transparentcolor")) == "white"
    is_geometry = root.geometry() == f"{sw}x{sh}+0+0"

    # Check the canvas' properties in the overlay that we set
    # We tagged the canvas that we made with "overlay"
    canvas = root.nametowidget(".overlay")
    is_canvas = canvas != None
    is_bg = canvas.cget("bg") == "white"
    is_highlightthickness = canvas.cget("highlightthickness") == "0"
    is_fill = canvas.pack_info().get("fill") == "both"
    is_expand = canvas.pack_info().get("expand") == True

    canvas_rectangle_id = canvas.find_withtag("overlay")[0]
    is_rectangle = canvas.type(canvas_rectangle_id) == "rectangle"
    is_coords = canvas.coords("overlay") == [border_thickness//2, border_thickness//2, sw - border_thickness//2, sh - border_thickness//2]
    is_outline = canvas.itemcget("overlay", "outline") == "green"
    is_width = float(canvas.itemcget("overlay", "width")) == border_thickness
    is_fill = canvas.itemcget("overlay", "fill") == "white"

    return ([
        is_root,
        is_overrideredirect,
        is_topmost,
        is_alpha,
        is_transparentcolor,
        is_geometry,

        is_canvas,
        is_bg,
        is_highlightthickness,
        is_fill,
        is_expand,

        is_rectangle,
        is_coords,
        is_outline,
        is_width,
        is_fill
    ])

def test_overlay_init():
    
    # Check for every property of root in the overlay that we set

    init_settings_test = get_overlay_init_tests()

    # We initialise the overlay window as withdrawn first
    is_withdrawn = root.state() == "withdrawn"

    assert all([
        *init_settings_test,
        is_withdrawn
    ])

def test_overlay_key():

    # Test that Ctrl + D works
    
    # Simulate a keystroke event

    # Simulate Ctrl
    key_simulator.press(keyboard.Key.ctrl_l)

    # Simulate D while holding Ctrl down
    key_simulator.press("d")

    # Release both
    key_simulator.release(keyboard.Key.ctrl_l)
    key_simulator.release("d")

    # Manually update the root window
    time.sleep(0.15)
    root.update()

    # The overlay should be on right now
    # Check all of the overlay init settings, and then check that the window is not withdrawn
    init_settings_test = get_overlay_init_tests()
    
    # root.deiconify() makes the state of root be "normal"
    is_deiconify = root.state() == "normal"

    assert all([
        *init_settings_test,
        is_deiconify
    ])

# Tests are run by pytest in the order they are defined
# Thus, this will be run right after test_overlay_key()
# Thus, Ctrl + D has already been pressed and overlay is on
def test_exit_key():

    # Test that Ctrl + D, then "a" properly turns off the overlay

    # Check that the overlay is properly initialised
    init_settings_test = get_overlay_init_tests()

    # Check that the overlay was on before
    is_deiconify_before = root.state() == "normal"

    # Simulate A
    key_simulator.press("a")
    # Release A
    key_simulator.release("a")

    # The gui_queue logic polls the queue once every 100ms
    # Thus wait for 150ms minimally to allow the gui_queue to catch the keypress
    time.sleep(0.15) # 0.15s = 150ms
    root.update()

    # Check that the overlay is withdrawn now
    is_withdrawn = root.state() == "withdrawn"
    print(root.state())
    assert all([
        *init_settings_test,
        is_deiconify_before,
        is_withdrawn
    ])

def test_wrong_key():

    # Check that the screen properly goes red, then turns off when a wrong key is pressed after Ctrl + D

    # Check that the overlay is properly initialised
    init_settings_test = get_overlay_init_tests()
    
    # Press Ctrl + D now
    # Simulate Ctrl
    key_simulator.press(keyboard.Key.ctrl_l)

    # Simulate D while holding Ctrl down
    key_simulator.press("d")

    # Release both
    key_simulator.release(keyboard.Key.ctrl_l)
    key_simulator.release("d")
    
    time.sleep(0.15)
    root.update()

    # Check that the overlay was on before
    is_deiconify_before = root.state() == "normal"
    # print(root.state())

    # Let the wrong keypress be F
    # Simulate F
    key_simulator.press("f")
    # Release F
    key_simulator.release("f")

    # Wait 150ms to allow the gui_queue polling loop to catch it
    time.sleep(0.15) # 0.15s = 150ms
    root.update()

    # Overlay should be red now
    canvas = root.nametowidget(".overlay")
    is_red = canvas.itemcget("overlay", "outline") == "red"

    # Red overlay is flashed for 1s
    # Thus wait 1.05s to allow the red overlay to go away
    time.sleep(1.05)
    root.update()

    # Overlay should be withdrawn now
    is_withdrawn = root.state() == "withdrawn"
    print(root.state())

    assert all([
        *init_settings_test,
        is_deiconify_before,
        is_red,
        is_withdrawn
    ])


# def test_control_panel_key():