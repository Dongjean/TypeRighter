from pynput import keyboard

key_simulator = keyboard.Controller()

import win32clipboard as clip
import win32con
from io import BytesIO
from helpers.main_test_helpers import wait, check_tk_exists, check_widget_props

def get_latex_build_tests(root, FONTS, COLORS):

    # Check if all the widgets exist
    latex_frame, is_latex_frame = check_tk_exists(root, "latex_frame")
    title_label, is_title_label = check_tk_exists(latex_frame, "title_label")
    subtitle_label, is_subtitle_label = check_tk_exists(latex_frame, "subtitle_label")
    editor_container, is_editor_container = check_tk_exists(latex_frame, "editor_container")
    text_editor, is_text_editor = check_tk_exists(editor_container, "text_editor")
    latex_output_container, is_latex_output_container = check_tk_exists(latex_frame, "latex_output_container")
    preview_label, is_preview_label = check_tk_exists(latex_output_container, "preview_label")
    latex_output_canvas, is_latex_output_canvas = check_tk_exists(preview_label, "latex_output_canvas")
    compile_button, is_compile_button = check_tk_exists(editor_container, "compile_button")

    # Check the properties of each widget

    # latex_frame
    # Get our desired latex_frame_props
    latex_frame_props = [
        ("config", "bg", COLORS["bg_main"]),
        ("config", "padx", 20),
        ("config", "pady", 20),
        ("config", "takefocus", "1"),

        ("pack", "side", "top"),
        ("pack", "fill", "both"),
        ("pack", "expand", True),

        ("misc", "widget_name", "latex_frame")
    ]
    is_latex_frame_props = check_widget_props(latex_frame, latex_frame_props)

    # title_label
    title_label_props = [
        ("config", "text", "LaTeX Equation Editor"),
        ("config", "bg", COLORS["bg_main"]),
        ("config", "fg", COLORS["text_main"]),

        ("pack", "fill", "x"),
        ("pack", "pady", 0),

        ("misc", "widget_name", "title_label"),

        ("misc", "font", FONTS["font_title"].actual())
    ]
    is_title_label_props = check_widget_props(title_label, title_label_props)

    # subtitle_label
    subtitle_label_props = [
        ("config", "text", "Edit and preview complex mathematical formulas"),
        ("config", "bg", COLORS["bg_main"]),
        ("config", "fg", COLORS["text_muted"]),

        ("pack", "fill", "x"),
        ("pack", "pady", (0, 15)),

        ("misc", "widget_name", "subtitle_label"),

        ("misc", "font", FONTS["font_subtitle"].actual())
    ]
    is_subtitle_label_props = check_widget_props(subtitle_label, subtitle_label_props)

    # editor_container
    editor_container_props = [
        ("config", "bg", COLORS["bg_input"]),
        ("config", "bd", 1),
        ("config", "highlightbackground", COLORS["border"]),
        ("config", "highlightthickness", 1),

        ("pack", "fill", "both"),
        ("pack", "expand", True),

        ("misc", "widget_name", "editor_container"),
    ]
    is_editor_container_props = check_widget_props(editor_container, editor_container_props)

    # text_editor
    text_editor_props = [
        ("config", "bg", COLORS["bg_input"]),
        ("config", "fg", COLORS["text_main"]),
        ("config", "insertbackground", "white"),
        ("config", "bd", 0),
        ("config", "padx", 15),
        ("config", "pady", 15),
        ("config", "wrap", "none"),

        ("pack", "fill", "both"),
        ("pack", "expand", True),

        ("misc", "widget_name", "text_editor"),

        ("misc", "font", FONTS["font_subtitle"].actual()),

        ("misc", "bind", "<Key-Return>"),
        ("misc", "bind", "<Shift-Key-Return>")
    ]
    is_text_editor_props = check_widget_props(text_editor, text_editor_props)

    # latex_output_container
    latex_output_container_props = [
        ("config", "bg", COLORS["bg_input"]),
        ("config", "bd", 1),
        ("config", "highlightbackground", COLORS["border"]),
        ("config", "highlightthickness", 1),
        ("config", "height", 150),

        ("pack", "fill", "x"),
        ("pack", "pady", (5, 20)),

        ("misc", "widget_name", "latex_output_container"),

        ("misc", "pack_propagate", False)
    ]
    is_latex_output_container_props = check_widget_props(latex_output_container, latex_output_container_props)

    # preview_label
    preview_label_props = [
        ("config", "bg", "white"),

        ("pack", "fill", "both"),
        ("pack", "expand", True),

        ("misc", "widget_name", "preview_label")
    ]
    is_preview_label_props = check_widget_props(preview_label, preview_label_props)

    # latex_output_canvas
    latex_output_canvas_props = [
        ("config", "bg", "white"),
        ("config", "highlightthickness", "0"),

        ("pack", "expand", True),

        ("misc", "widget_name", "latex_output_canvas")
    ]
    is_latex_output_canvas_props = check_widget_props(latex_output_canvas, latex_output_canvas_props)

    # compile_button
    compile_button_props = [
        ("config", "text", "Compile"),
        ("config", "bg", COLORS["border"]),
        ("config", "fg", COLORS["text_main"]),
        ("config", "bd", 0),
        ("config", "relief", "flat"),
        ("config", "command", True), # Check that a function is linked to command

        ("pack", "side", "right"),

        ("misc", "widget_name", "compile_button"),

        ("misc", "font", FONTS["font_subtitle"].actual())
    ]
    is_compile_button_props = check_widget_props(compile_button, compile_button_props)

    # root
    root_props = [
        ("misc", "bind", "<Key-Return>"),
        ("misc", "bind", "<Shift-Key-Return>")
    ]
    is_root_props = check_widget_props(root, root_props)

    return {
        "is_latex_frame": is_latex_frame,
        "is_title_label": is_title_label,
        "is_subtitle_label": is_subtitle_label,
        "is_editor_container": is_editor_container,
        "is_text_editor": is_text_editor,
        "is_latex_output_container": is_latex_output_container,
        "is_preview_label": is_preview_label,
        "is_latex_output_canvas": is_latex_output_canvas,
        "is_compile_button": is_compile_button,
        "is_latex_frame_props": is_latex_frame_props,
        "is_title_label_props": is_title_label_props,
        "is_subtitle_label_props": is_subtitle_label_props,
        "is_editor_container_props": is_editor_container_props,
        "is_text_editor_props": is_text_editor_props,
        "is_latex_output_container_properties": is_latex_output_container_props,
        "is_preview_label_props": is_preview_label_props,
        "is_latex_output_canvas_props": is_latex_output_canvas_props,
        "is_compile_button_props": is_compile_button_props,
        "is_root_props": is_root_props
    }

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