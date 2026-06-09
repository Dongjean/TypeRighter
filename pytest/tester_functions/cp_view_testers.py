import sys
from pynput import keyboard

# Key simulator
key_simulator = keyboard.Controller()

from helper_functions.main_test_helpers import wait
from helper_functions.overlay_view_test_helpers import get_overlay_init_tests
from helper_functions.latex_window_test_helpers import get_latex_build_tests
from helper_functions.navbar_component_test_helpers import get_navbar_build_tests
from helper_functions.cp_view_test_helpers import get_cp_init_tests

def helper_test_control_panel_key(test_env, subtests):

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