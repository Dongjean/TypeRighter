from pynput import keyboard

key_simulator = keyboard.Controller()

from helper_functions.main_test_helpers import wait
from helper_functions.overlay_view_test_helpers import get_overlay_init_tests

border_thickness = 5

def helper_test_bg_listener_on(test_env, subtests):
    
    root, sw, sh, FONTS, COLORS, WINDOWS = test_env

    # Trigger the COMBINATION keybind to turn on the overlay
    key_simulator.press(keyboard.Key.ctrl_l)
    key_simulator.press(keyboard.Key.alt_l)
    key_simulator.press(keyboard.Key.space)

    wait(root, 0.05)

    key_simulator.release(keyboard.Key.ctrl_l)
    key_simulator.release(keyboard.Key.alt_l)
    key_simulator.release(keyboard.Key.space)

    # Check that the overlay is properly initiated
    init_settings_test = get_overlay_init_tests(root, sw, sh)

    # We initialise the overlay window as withdrawn first
    is_deiconify = root.state() == "normal"

    all_assertions = {
        **init_settings_test,
        "is_deiconify": is_deiconify
    }
    
    for key, assertion in all_assertions.items():
        with subtests.test(msg=f"Asserting {key}"):
            assert assertion