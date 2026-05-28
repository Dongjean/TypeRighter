import pytest

import sys

import main as main

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

def get_cp_init_tests():

    # All of these should be True

    is_root = root != None
    is_title = root.title() == "TypeRighter - Control Panel"

    # There is a known bug with tkinter, where root.overrideredirect() == None when we set it to False
    # This is because setting it to False gives control of the title bar and borders to the native OS
    # The windows OS returns 0, but for some reason tkinter's internal boolean converters converts that to None
    is_overrideredirect = root.overrideredirect() == None
    is_topmost = root.attributes("-topmost") == False
    is_alpha = root.attributes("-alpha") == 1
    is_transparentcolor = False
    if sys.platform.startswith("win"):
        is_transparentcolor = str(root.attributes("-transparentcolor")) == ""
    elif sys.platform.startswith("linux"):
        # Just skip the test by letting it pass
        is_transparentcolor = True
    else:
        is_transparentcolor = str(root.attributes("-transparentcolor")) == ""
    is_geometry = root.geometry() == "1050x720+0+0"
    print(is_geometry)
    is_bg_white = root.cget("bg") == "#ffffff"

    # Check that there is no overlay canvas anymore
    is_overlay_gone = False
    try:
        # Try to access the overlay_canvas
        root.nametowidget(".overlay")
    except KeyError:
        # If we cannot find it because any child widget with the name "overlay" cannot be found, then overlay is truly gone
        is_overlay_gone = True

    # Check that it is not withdrawn
    is_deiconify = root.state() == "normal"

    return {
        "is_root": is_root,
        "is_title": is_title,
        "is_overrideredirect": is_overrideredirect,
        "is_topmost": is_topmost,
        "is_alpha": is_alpha,
        "is_transparentcolor": is_transparentcolor,
        "is_geometry": is_geometry,
        "is_bg_white": is_bg_white,

        "is_overlay_gone": is_overlay_gone,

        "is_deiconify": is_deiconify
    }

def check_tk_exists(parent, child_name):
    try:

        # Widget with name child_name exists under the widget parent
        child_widget = parent.nametowidget(child_name)
        return (child_widget, True)
    except KeyError:

        # Widget with name child_name does not exist under the widget parent
        return (None, False)
    except AttributeError:

        # The widget parent doesnt exist
        return (None, False)
def get_latex_build_tests():

    # All of these should be True

    latex_frame, is_latex_frame = check_tk_exists(root, "latex_frame")
    title_label, is_title_label = check_tk_exists(latex_frame, "title_label")
    subtitle_label, is_subtitle_label = check_tk_exists(latex_frame, "subtitle_label")
    editor_container, is_editor_container = check_tk_exists(latex_frame, "editor_container")
    text_editor, is_text_editor = check_tk_exists(editor_container, "text_editor")
    latex_output_container, is_latex_output_container = check_tk_exists(latex_frame, "latex_output_container")
    preview_label, is_preview_label = check_tk_exists(latex_output_container, "preview_label")
    latex_output_canvas, is_latex_output_canvas = check_tk_exists(preview_label, "latex_output_canvas")
    compile_button, is_compile_button = check_tk_exists(editor_container, "compile_button")

    return {
        "is_latex_frame": is_latex_frame,
        "is_title_label": is_title_label,
        "is_subtitle_label": is_subtitle_label,
        "is_editor_container": is_editor_container,
        "is_text_editor": is_text_editor,
        "is_latex_output_container": is_latex_output_container,
        "is_preview_label": is_preview_label,
        "is_latex_output_canvas": is_latex_output_canvas,
        "is_compile_button": is_compile_button
    }

def test_overlay_init(subtests):
    
    # Check for every property of root in the overlay that we set

    init_settings_test = get_overlay_init_tests()

    # We initialise the overlay window as withdrawn first
    is_withdrawn = root.state() == "withdrawn"

    all_assertions = {
        **init_settings_test,
        "is_withdrawn": is_withdrawn
    }

    for key, assertion in all_assertions.items():
        with subtests.test(msg=f"Asserting {key}"):
            assert assertion

def test_overlay_key(subtests):

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

    all_assertions = {
        **init_settings_test,
        "is_deiconify": is_deiconify
    }

    for key, assertion in all_assertions.items():
        with subtests.test(msg=f"Asserting {key}"):
            assert assertion

# Tests are run by pytest in the order they are defined
# Thus, this will be run right after test_overlay_key()
# Thus, Ctrl + D has already been pressed and overlay is on
def test_exit_key(subtests):

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
    all_assertions = {
        **init_settings_test,
        "is_deiconify_before": is_deiconify_before,
        "is_withdrawn": is_withdrawn
    }

    for key, assertion in all_assertions.items():
        with subtests.test(msg=f"Asserting {key}"):
            assert assertion

def test_wrong_key(subtests):

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

    all_assertions = {
        **init_settings_test,
        "is_deiconify_before": is_deiconify_before,
        "is_red": is_red,
        "is_withdrawn": is_withdrawn
    }

    for key, assertion in all_assertions.items():
        with subtests.test(msg=f"Asserting {key}"):
            assert assertion

def test_control_panel_key(subtests):

    # Check that the control panel properly opens, with the LaTeX editor as the default first window

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

    # Press \ to open the control panel
    # Simulate \
    key_simulator.press("\\")
    # Release \
    key_simulator.release("\\")

    # Wait 150ms to allow the gui_queue polling loop to catch it
    time.sleep(0.15) # 0.15s = 150ms
    root.update()

    # Now, check the control panel init options
    cp_init_settings_test = get_cp_init_tests()

    # Now, check the LaTeX editor build options
    latex_build_settings_test = get_latex_build_tests()

    all_assertions = {
        **latex_build_settings_test,
        **cp_init_settings_test,
        "is_deiconify_before": is_deiconify_before
    }

    for key, assertion in all_assertions.items():
        with subtests.test(msg=f"Asserting {key}"):
            assert assertion