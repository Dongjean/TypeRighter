import sys
from pynput import keyboard

# Key simulator
key_simulator = keyboard.Controller()

from helper_functions.main_test_helpers import wait, check_tk_exists
from helper_functions.overlay_view_test_helpers import get_overlay_init_tests
from helper_functions.latex_window_test_helpers import get_latex_build_tests
from helper_functions.navbar_component_test_helpers import get_navbar_build_tests
from helper_functions.cp_view_test_helpers import get_cp_init_tests

from tester_functions.overlay_view_testers import helper_test_overlay_breakout_key_on, helper_test_overlay_breakout_key_off

def helper_test_control_panel_key(test_env, subtests):

    root, sw, sh, FONTS, COLORS, WINDOWS = test_env
    
    helper_test_overlay_breakout_key_on(test_env, subtests)
    
    # In the systematic test environment, s is mapped to Control Panel Open
    key_simulator.press("s")

    wait(root, 0.5)

    command_textbox, is_command_textbox = check_tk_exists(root, "textbox")
    command_prompt, is_command_prompt = check_tk_exists(command_textbox, "typed")
    command_preview, is_command_preview = check_tk_exists(command_textbox, "preview")

    is_command_displayed = command_prompt.cget("text") == "s" # Typed command display is correct
    is_command_color = command_prompt.cget("fg") == "white" # Typed command display is white, not red
    is_preview = command_preview.cget("text") == "Control Panel" # Command preview is properly displaying

    # Release breakout key and check that control panel opens
    helper_test_overlay_breakout_key_off(test_env, subtests)

    wait(root, 0.5)

    # Now, check the control panel init options
    cp_init_settings_test = get_cp_init_tests(root, sw, sh)

    # Now, check the LaTeX editor build options
    latex_build_settings_test = get_latex_build_tests(root, FONTS, COLORS)

    # Now, check that the NavBar is properly built
    # navbar_build_settings_test = get_navbar_build_tests(root, FONTS, COLORS, WINDOWS, "latex-workspace")

    all_assertions = {
        "is_command_displayed": is_command_displayed,
        "is_command_color": is_command_color,
        "is_preview": is_preview,
        **cp_init_settings_test,
        **latex_build_settings_test,
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