import pytest
from tkinter import font as tkfont
import tkinter as tk
import win32clipboard as clip
import win32con
from io import BytesIO

import sys

import main as main

import time
from pynput import keyboard

# Import helper functions
from helpers.main_test_helpers import wait, check_tk_exists
from helpers.overlay_view_test_helpers import get_overlay_init_tests
from helpers.cp_view_test_helpers import get_cp_init_tests
from helpers.latex_window_test_helpers import get_latex_build_tests
from helpers.navbar_component_test_helpers import get_navbar_build_tests

border_thickness = 5
key_simulator = keyboard.Controller()


@pytest.fixture(scope="module")
def test_env():

    # This part runs before the test_ functions

    # Initialise the tkinter root window and the pynput listener
    # Manually initialize the tkinter window without .mainloop()
    # Run root_view.root_init()
    root = main.view_handler.root_init()
    root.update()

    # Start a completely new pynput thread
    # pynput threads cannot be reused
    listener = keyboard.Listener(on_press=lambda key: main.on_press_bg(key, listener), on_release=lambda key: main.on_release_bg(key, listener))
    listener.start()

    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()

    # Custom Fonts
    FONTS = {
        "font_title": tkfont.Font(family="Segoe UI", size=16, weight="bold"),
        "font_subtitle": tkfont.Font(family="Segoe UI", size=10, weight="normal"),
        "font_hyperlink": tkfont.Font(family="Segoe UI", size=10, weight="normal", underline=True),
    }

    # Color Palette
    COLORS = {
        "bg_main": "#202020",
        "bg_input": "#1a1a1a",
        "text_main": "#e3e3e3",
        "text_muted": "#888888",
        "border": "#2d2d2d",
        "accent_blue": "#2a5a9c",
        "hyperlink_blue": "#0099FF",
    }

    # Windows
    WINDOWS = {
        "latex-workspace": {
            "name": "LaTeX",
            "icon": "",
        },
        "user-auth": {
            "name": "Login",
            "icon": "",
        }
    }

    yield (root, sw, sh, FONTS, COLORS, WINDOWS) # This is where the code runs

    # This is after all the tests
    # Close everything
    
    # Destroy the root window
    main.view_handler.gui_queue.put("destroy_root")

    # Stop the pynput listener
    main.stop_all_pynput_keyboard_listeners()

    # Sleep for 150ms to let the tkinter root window properly close
    wait(root, 0.15)

    # Delete all .after() instances
    try:
        for after_id in root.eval('after info').split():
            print(after_id)
            root.after_cancel(after_id)
    except Exception as e:
        print(e)

def test_overlay_init(test_env, subtests):
    
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

def test_control_panel_key(test_env, subtests):

    root, sw, sh, FONTS, COLORS, WINDOWS = test_env

    # Check that the control panel properly opens, with the LaTeX editor as the default first window

    # Press Ctrl + D now
    # Simulate Ctrl
    key_simulator.press(keyboard.Key.ctrl_l)

    # Simulate D while holding Ctrl down
    key_simulator.press("d")

    # Release both
    key_simulator.release(keyboard.Key.ctrl_l)
    key_simulator.release("d")
    
    wait(root, 0.15)
    # time.sleep(5)
    # Check that the overlay was on before
    is_deiconify_before = root.state() == "normal"
    print("this")
    print(is_deiconify_before)
    print(root.state())
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
# The LaTeX window is open, test the LaTeX window
def test_latex_output_enter(test_env, subtests):

    root, sw, sh, FONTS, COLORS, WINDOWS = test_env

    # Check that typing into the latex editor and pressing enter gives us a valid latex output, and saves the output to our clipboard

    # Bring active focus to the LaTeX editor
    latex_frame, is_latex_frame = check_tk_exists(root, "latex_frame")
    editor_container, is_editor_container = check_tk_exists(latex_frame, "editor_container")
    text_editor, is_text_editor = check_tk_exists(editor_container, "text_editor")
    text_editor.focus_set()

    # Simulate typing out a latex formula
    latex_code_sample = r"\frac{1}{3}"
    for char in latex_code_sample:
        key_simulator.press(char)
    
    # Press Enter to compile
    key_simulator.press(keyboard.Key.enter)

    # Wait a little bit to allow some buffer time for the LaTeX output to be processed
    wait(root, 0.15)

    # Check that we received and properly displayed the LaTeX output
    latex_output_container, is_latex_output_container = check_tk_exists(latex_frame, "latex_output_container")
    preview_label, is_preview_label = check_tk_exists(latex_output_container, "preview_label")
    latex_output_canvas, is_latex_output_canvas = check_tk_exists(preview_label, "latex_output_canvas")
    tk_img = None
    pil_img = None
    try:
        tk_img = latex_output_canvas.image
        pil_img = latex_output_canvas.pil_img
    except AttributeError:
        pass

    # LaTeX output is properly displayed iff both of these have a value, if not something is wrong
    is_latex_output_displayed = (tk_img != None) and (pil_img != None)

    # Check that an image is properly copied to clipboard
    clip_data = None
    clip.OpenClipboard()
    try:
        clip_data = clip.GetClipboardData(win32con.CF_DIB)
    finally:
        clip.CloseClipboard()
    # Check if an image is copied at all
    is_img_copied = (clip_data != None)
    
    # Check if the image copied is the right image
    # Get the dib data from pil_img
    rgba_img = pil_img.convert("RGBA")
    output = BytesIO()
    rgba_img.save(output, "BMP")
    dib_data = output.getvalue()[14:]
    output.close()
    is_latex_img_copied = (pil_img != None) and (clip_data == dib_data)

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

    all_assertions = {
        "is_latex_output_displayed": is_latex_output_displayed,
        "is_img_copied": is_img_copied,
        "is_latex_img_copied": is_latex_img_copied
    }

    for key, assertion in all_assertions.items():
        with subtests.test(msg=f"Asserting {key}"):
            assert assertion