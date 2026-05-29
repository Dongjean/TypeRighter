import pytest
from tkinter import font as tkfont

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

# Custom Fonts
FONTS = {
    "font_title": tkfont.Font(family="Segoe UI", size=16, weight="bold"),
    "font_subtitle": tkfont.Font(family="Segoe UI", size=10, weight="normal"),
    "font_hyperlink": tkfont.Font(family="Segoe UI", size=10, weight="normal", underline=True),
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
    is_geometry = root.geometry() == f"{sw // 2}x{sh // 2}+0+0"
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

    # Check that we have the root keybind to <Button-1>
    is_root_bind = check_widget_props(root, [("misc", "bind", "<Button-1>")])

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

        "is_deiconify": is_deiconify,

        "is_root_bind": is_root_bind
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

def check_widget_props(widget, props):
    widget_pack_info = None
    widget_binds = None
    try:
        widget_pack_info = widget.pack_info()
    except AttributeError as e:
        print(e)
    try:
        widget_binds = widget.bind()
    except AttributeError as e:
        print(e)
    curr_props = [

        # Command prop (Check that the function exists only)
        (prop[0], prop[1], True if widget.cget(prop[1]) else False) if prop[0] == "config" and prop[1] == "command"
        else
        # variable prop (for RadioButton)
        (prop[0], prop[1], str(widget.cget(prop[1]))) if prop[0] == "config" and prop[1] == "variable"
        else
        # Config props
        (prop[0], prop[1], widget.cget(prop[1])) if prop[0] == "config"
        else
        # Pack props
        (prop[0], prop[1], widget_pack_info[prop[1]]) if prop[0] == "pack"
        else
        # Widget name prop
        (prop[0], prop[1], widget.winfo_name()) if prop[0] == "misc" and prop[1] == "widget_name"
        else
        # Font prop
        (prop[0], prop[1], tkfont.nametofont(widget.cget("font")).actual()) if prop[0] == "misc" and prop[1] == "font"
        else
        # pack_propagate prop
        (prop[0], prop[1], widget.tk.call('pack', 'propagate', widget._w)) if prop[0] == "misc" and prop[1] == "pack_propagate"
        else
        # Bind prop
        (prop[0], prop[1], prop[2] if prop[2] in widget_binds else None) if prop[0] == "misc" and prop[1] == "bind"
        else
        # Python syntax demands a fallback
        (prop[0], prop[1], prop[2])
        for prop in props
    ]
    print(curr_props)
    is_widget_props = all([
        curr_props[index] == prop for index, prop in enumerate(props)
    ])
    
    return is_widget_props

def get_latex_build_tests():

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

def get_navbar_build_tests():

    # Check if all the widgets exist
    navbar_frame, is_navbar_frame = check_tk_exists(root, "navbar_frame")

    # Check the properties of navbar_frame
    navbar_frame_props = [
        ("config", "bg", COLORS["bg_main"]),
        ("config", "takefocus", '1'),

        ("pack", "side", "right"),
        ("pack", "fill", "both"),

        ("misc", "widget_name", "navbar_frame")
    ]
    is_navbar_frame_props = check_widget_props(navbar_frame, navbar_frame_props)

    # Check each window selector widget
    is_window_selections = True
    is_window_selections_props = True # If there are theoretically no window selections resolved, this is vacuously true
    for key, value in WINDOWS.items():

        # Check if this window selector exists
        curr_window_selector, is_curr_window_selector = check_tk_exists(navbar_frame, key)
        # If even a single window selector doesnt exist, fail the check
        if not is_curr_window_selector:
            is_window_selections = False
        
        # Check for the props of the window selector, if it exists
        if is_curr_window_selector:
            
            curr_window_selector_props = [
                ("config", "text", value["name"]),
                ("config", "variable", str(navbar_frame.selected_window)),
                ("config", "value", key),
                ("config", "bg", COLORS["border"]),
                ("config", "fg", COLORS["text_main"]),
                ("config", "bd", 0),
                ("config", "relief", "flat"),
                ("config", "width", 10),
                ("config", "height", 3),
                ("config", "selectcolor", COLORS["accent_blue"]),
                ("config", "activebackground", COLORS["accent_blue"]),
                ("config", "indicatoron", False),
                ("config", "command", True),

                ("pack", "side", "top"),

                ("misc", "widget_name", key),

                ("misc", "font", FONTS["font_subtitle"].actual())
            ]
            is_curr_window_selector = check_widget_props(curr_window_selector, curr_window_selector_props)
            # If even a single window selector's props is invalid, fail the check
            if not is_curr_window_selector:
                is_window_selections_props = False
    
    # Check that the current, default, selected window is the LaTeX window
    is_default_window_selected = navbar_frame.selected_window.get() == "latex-workspace"

    return {
        "is_navbar_frame": is_navbar_frame,
        "is_navbar_frame_props": is_navbar_frame_props,
        "is_window_selections": is_window_selections,
        "is_window_selections_props": is_window_selections_props,
        "is_default_window_selected": is_default_window_selected
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

    # Now, check that the NavBar is properly built
    navbar_build_settings_test = get_navbar_build_tests()

    all_assertions = {
        **latex_build_settings_test,
        **cp_init_settings_test,
        **navbar_build_settings_test,
        "is_deiconify_before": is_deiconify_before
    }

    for key, assertion in all_assertions.items():
        with subtests.test(msg=f"Asserting {key}"):
            assert assertion