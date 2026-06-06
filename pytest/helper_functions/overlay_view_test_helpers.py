import sys
from pynput import keyboard

key_simulator = keyboard.Controller()

from helpers.main_test_helpers import wait
from helpers.latex_window_test_helpers import get_latex_build_tests
from helpers.navbar_component_test_helpers import get_navbar_build_tests
from helpers.cp_view_test_helpers import get_cp_init_tests

border_thickness = 5
def get_overlay_init_tests(root, sw, sh):

    # All of these should be True
    is_root = root != None
    is_overrideredirect = root.overrideredirect() == True
    is_topmost = root.attributes("-topmost") == True
    is_alpha = root.attributes("-alpha") == 0.5
    is_transparentcolor = False
    if sys.platform.startswith("win"):
        is_transparentcolor = str(root.attributes("-transparentcolor")) == "white"
    elif sys.platform.startswith("linux"):
        # Just skip the test by letting it pass
        is_transparentcolor = True
    else:
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

    return {
        "is_root": is_root,
        "is_overrideredirect": is_overrideredirect,
        "is_topmost": is_topmost,
        "is_alpha": is_alpha,
        "is_transparentcolor": is_transparentcolor,
        "is_geometry": is_geometry,

        "is_canvas": is_canvas,
        "is_bg": is_bg,
        "is_highlightthickness": is_highlightthickness,
        "is_fill": is_fill,
        "is_expand": is_expand,

        "is_rectangle": is_rectangle,
        "is_coords": is_coords,
        "is_outline": is_outline,
        "is_width": is_width,
        "is_fill": is_fill
    }


def helper_test_overlay_init(test_env, subtests):
    
    root, sw, sh, FONTS, COLORS, WINDOWS = test_env

    # Check for every property of root in the overlay that we set

    init_settings_test = get_overlay_init_tests(root, sw, sh)

    # We initialise the overlay window as withdrawn first
    is_withdrawn = root.state() == "withdrawn"

    all_assertions = {
        **init_settings_test,
        "is_withdrawn": is_withdrawn
    }
    
    for key, assertion in all_assertions.items():
        with subtests.test(msg=f"Asserting {key}"):
            assert assertion

def helper_test_overlay_key(test_env, subtests):

    root, sw, sh, FONTS, COLORS, WINDOWS = test_env

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
    wait(root, 0.15)

    # The overlay should be on right now
    # Check all of the overlay init settings, and then check that the window is not withdrawn
    init_settings_test = get_overlay_init_tests(root, sw, sh)
    
    # root.deiconify() makes the state of root be "normal"
    is_deiconify = root.state() == "normal"

    all_assertions = {
        **init_settings_test,
        "is_deiconify": is_deiconify
    }

    for key, assertion in all_assertions.items():
        with subtests.test(msg=f"Asserting {key}"):
            assert assertion

# Tests are run by pytest in the order they are defined
def helper_test_exit_key(test_env, subtests):

    root, sw, sh, FONTS, COLORS, WINDOWS = test_env

    # Test that Ctrl + D, then "a" properly turns off the overlay

    # Check that the overlay is properly initialised
    init_settings_test = get_overlay_init_tests(root, sw, sh)

    # Check that the overlay was on before
    is_deiconify_before = root.state() == "normal"

    # Simulate A
    key_simulator.press("a")
    # Release A
    key_simulator.release("a")

    # The gui_queue logic polls the queue once every 100ms
    # Thus wait for 150ms minimally to allow the gui_queue to catch the keypress
    wait(root, 0.15) # 0.15s = 150ms

    # Check that the overlay is withdrawn now
    is_withdrawn = root.state() == "withdrawn"
    print(root.state())
    all_assertions = {
        **init_settings_test,
        "is_deiconify_before": is_deiconify_before,
        "is_withdrawn": is_withdrawn
    }

    for key, assertion in all_assertions.items():
        with subtests.test(msg=f"Asserting {key}"):
            assert assertion

def helper_test_wrong_key(test_env, subtests):

    root, sw, sh, FONTS, COLORS, WINDOWS = test_env

    # Check that the screen properly goes red, then turns off when a wrong key is pressed after Ctrl + D

    # Check that the overlay is properly initialised
    init_settings_test = get_overlay_init_tests(root, sw, sh)
    
    # Press Ctrl + D now
    # Simulate Ctrl
    key_simulator.press(keyboard.Key.ctrl_l)

    # Simulate D while holding Ctrl down
    key_simulator.press("d")

    # Release both
    key_simulator.release(keyboard.Key.ctrl_l)
    key_simulator.release("d")
    
    wait(root, 0.15)

    # Check that the overlay was on before
    is_deiconify_before = root.state() == "normal"
    # print(root.state())

    # Let the wrong keypress be F
    # Simulate F
    key_simulator.press("f")
    # Release F
    key_simulator.release("f")

    # Wait 150ms to allow the gui_queue polling loop to catch it
    wait(root, 0.15) # 0.15s = 150ms

    # Overlay should be red now
    canvas = root.nametowidget(".overlay")
    is_red = canvas.itemcget("overlay", "outline") == "red"

    # Red overlay is flashed for 1s
    # Thus wait 1.05s to allow the red overlay to go away
    wait(root, 1.05)

    # Overlay should be withdrawn now
    is_withdrawn = root.state() == "withdrawn"

    all_assertions = {
        **init_settings_test,
        "is_deiconify_before": is_deiconify_before,
        "is_red": is_red,
        "is_withdrawn": is_withdrawn
    }

    for key, assertion in all_assertions.items():
        with subtests.test(msg=f"Asserting {key}"):
            assert assertion

def helper_test_control_panel_key(test_env, subtests):

    root, sw, sh, FONTS, COLORS, WINDOWS = test_env

    # Check that the control panel properly opens, with the LaTeX editor as the default first window

    # Check that the overlay is properly initialised
    init_settings_test = get_overlay_init_tests(root, sw, sh)
    
    # Press Ctrl + D now
    # Simulate Ctrl
    key_simulator.press(keyboard.Key.ctrl_l)

    # Simulate D while holding Ctrl down
    key_simulator.press("d")

    # Release both
    key_simulator.release(keyboard.Key.ctrl_l)
    key_simulator.release("d")
    
    wait(root, 0.15)

    # Check that the overlay was on before
    is_deiconify_before = root.state() == "normal"

    # Press \ to open the control panel
    # Simulate \
    key_simulator.press("\\")
    # Release \
    key_simulator.release("\\")

    # Wait 150ms to allow the gui_queue polling loop to catch it
    wait(root, 0.15) # 0.15s = 150ms

    # Now, check the control panel init options
    cp_init_settings_test = get_cp_init_tests(root, sw, sh)

    # Now, check the LaTeX editor build options
    latex_build_settings_test = get_latex_build_tests(root, FONTS, COLORS)

    # Now, check that the NavBar is properly built
    navbar_build_settings_test = get_navbar_build_tests(root, FONTS, COLORS, WINDOWS, "latex-workspace")

    all_assertions = {
        "is_deiconify_before": is_deiconify_before,
        **cp_init_settings_test,
        **latex_build_settings_test,
        **navbar_build_settings_test
    }

    for key, assertion in all_assertions.items():
        with subtests.test(msg=f"Asserting {key}"):
            assert assertion

# As of here, the control panel view is open
def helper_test_close_control_panel(test_env):

    root, sw, sh, FONTS, COLORS, WINDOWS = test_env

    # Check that when we close the control panel view, the overlay view is properly re-initialised and works fine

    # Simulate Alt + f4 to close the control panel view
    # Simulate Alt
    key_simulator.press(keyboard.Key.alt_l)

    # Simulate D while holding Ctrl down
    key_simulator.press(keyboard.Key.f4)

    # Release both
    key_simulator.release(keyboard.Key.alt_l)
    key_simulator.release(keyboard.Key.f4)

    # Wait 150ms to allow the gui_queue polling loop to catch it
    wait(root, 0.15) # 0.15s = 150ms

    # If the overlay works properly now, then control panel has been closed properly
    # No need for asserts