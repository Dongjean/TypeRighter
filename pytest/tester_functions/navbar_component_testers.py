from pynput import keyboard

key_simulator = keyboard.Controller()

from helper_functions.main_test_helpers import wait, check_tk_exists
from helper_functions.navbar_component_test_helpers import get_navbar_build_tests
from helper_functions.latex_window_test_helpers import get_latex_build_tests
from helper_functions.user_auth_window_test_helpers import get_user_auth_build_tests
from helper_functions.unicode_window_test_helpers import get_unicode_menu_build_test
from helper_functions.settings_window_test_helpers import get_settings_window_build_test

TEST_FUNCS = {
    "latex-workspace": get_latex_build_tests,
    "user-auth": get_user_auth_build_tests,
    "unicode-search": get_unicode_menu_build_test,
    "settings-window": lambda *args, **kwargs: True, # Placeholder empty settings window build tester
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