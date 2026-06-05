from pynput import keyboard

key_simulator = keyboard.Controller()

from helpers.main_test_helpers import wait, check_tk_exists, check_widget_props
from helpers.latex_window_test_helpers import get_latex_build_tests
from helpers.user_auth_window_test_helpers import get_user_auth_build_tests

def get_navbar_build_tests(root, FONTS, COLORS, WINDOWS, curr_window):

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
    is_default_window_selected = navbar_frame.selected_window.get() == curr_window

    return {
        "is_navbar_frame": is_navbar_frame,
        "is_navbar_frame_props": is_navbar_frame_props,
        "is_window_selections": is_window_selections,
        "is_window_selections_props": is_window_selections_props,
        "is_default_window_selected": is_default_window_selected
    }

TEST_FUNCS = {
    "latex-workspace": get_latex_build_tests,
    "user-auth": get_user_auth_build_tests,
}

# As of here, the control panel view is open
# The LaTeX window is open, test the LaTeX window
def helper_test_navbar(test_env, subtests):

    root, sw, sh, FONTS, COLORS, WINDOWS = test_env

    # Check that typing into the latex editor and pressing enter gives us a valid latex output, and saves the output to our clipboard

    navbar_frame, is_navbar_frame = check_tk_exists(root, "navbar_frame")
    # For each window, select it and perform build test on the resulting windows
    window_navbar_tests = {}
    window_build_tests = {}
    for key, value in WINDOWS.items():
        # Select the current window
        curr_window_selector = navbar_frame.nametowidget(key)
        curr_window_selector.invoke()
        # Give it some short buffer time to change windows fully
        wait(root, 0.05)
        window_navbar_tests[key + "_navbar"] = get_navbar_build_tests(root, FONTS, COLORS, WINDOWS, key)

        # Perform the respective initialisation tests for each resulting window
        window_build_tests[key + "_build"] = TEST_FUNCS[key](root, FONTS, COLORS)
    
    root.update()

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
        **window_navbar_tests,
        **window_build_tests,
    }

    for key, assertion in all_assertions.items():
        with subtests.test(msg=f"Asserting {key}"):
            assert assertion