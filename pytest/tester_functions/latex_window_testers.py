from pynput import keyboard

key_simulator = keyboard.Controller()

import win32clipboard as clip
import win32con
from io import BytesIO
from helper_functions.main_test_helpers import wait, check_tk_exists

# The LaTeX window is open, test the LaTeX window
def helper_test_latex_output_enter(test_env, subtests):

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