from pynput import keyboard

key_simulator = keyboard.Controller()

from helper_functions.main_test_helpers import check_tk_exists, check_widget_props

def get_navbar_build_tests(root, FONTS, COLORS, WINDOWS, curr_window):

    # Check if all the widgets exist
    navbar_frame, is_navbar_frame = check_tk_exists(root, "navbar_frame")

    # Check the properties of navbar_frame
    navbar_frame_props = [
        ("config", "bg", COLORS["bg_main"]),
        ("config", "takefocus", '1'),
        ("config", "width", 10),

        ("pack", "side", "right"),
        ("pack", "fill", "y"),

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
            print('here')
            is_window_selections = False
            break
        
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
                ("config", "height", 3),
                ("config", "selectcolor", COLORS["accent_blue"]),
                ("config", "activebackground", COLORS["accent_blue"]),
                ("config", "indicatoron", False),
                ("config", "command", True),

                ("pack", "side", "top"),
                ("pack", "fill", "x"),

                ("misc", "widget_name", key),

                ("misc", "font", FONTS["font_subtitle"].actual())
            ]
            is_curr_window_selector_props = check_widget_props(curr_window_selector, curr_window_selector_props)
            # If even a single window selector's props is invalid, fail the check
            if not is_curr_window_selector_props:
                print(curr_window_selector)
                is_window_selections_props = False
                break
    
    # Check that the current, default, selected window is the LaTeX window
    is_default_window_selected = navbar_frame.selected_window.get() == curr_window

    return {
        "is_navbar_frame": is_navbar_frame,
        "is_navbar_frame_props": is_navbar_frame_props,
        "is_window_selections": is_window_selections,
        "is_window_selections_props": is_window_selections_props,
        "is_default_window_selected": is_default_window_selected
    }
