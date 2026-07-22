import sys
from pynput import keyboard

key_simulator = keyboard.Controller()

from tester_functions.bg_listener_testers import helper_test_bg_listener_on, helper_test_bg_listener_off

from helper_functions.main_test_helpers import wait, check_tk_exists
from helper_functions.overlay_view_test_helpers import get_overlay_init_tests

import main as main

border_thickness = 5

def helper_test_overlay_breakout_key_on(test_env, subtests):
    
    root, sw, sh, FONTS, COLORS, WINDOWS = test_env
    
    key_simulator.press("\\")

    wait(root, 0.1)

    command_textbox, is_command_textbox = check_tk_exists(root, "textbox")

    # Test command popup if its open
    is_deiconify = command_textbox.state() == "normal"

    all_assertions = {
        "is_deiconify": is_deiconify
    }
    
    for key, assertion in all_assertions.items():
        with subtests.test(msg=f"Asserting {key}"):
            assert assertion

def helper_test_overlay_breakout_key_off(test_env, subtests):
    
    root, sw, sh, FONTS, COLORS, WINDOWS = test_env
    
    key_simulator.release("\\")

    wait(root, 0.1)

    command_textbox, is_command_textbox = check_tk_exists(root, "textbox")

    # Test command popup if its closed
    is_withdrawn = command_textbox.state() == "withdrawn"

    all_assertions = {
        "is_withdrawn": is_withdrawn
    }
    
    for key, assertion in all_assertions.items():
        with subtests.test(msg=f"Asserting {key}"):
            assert assertion

# def helper_test_overlay(test_env, subtests):

#     root, sw, sh, FONTS, COLORS, WINDOWS = test_env

#     # Test that Ctrl + D works
    
#     # Simulate a keystroke event

#     # Simulate Ctrl
#     key_simulator.press(keyboard.Key.ctrl_l)

#     # Simulate D while holding Ctrl down
#     key_simulator.press("d")

#     # Release both
#     key_simulator.release(keyboard.Key.ctrl_l)
#     key_simulator.release("d")

#     # Manually update the root window
#     wait(root, 0.15)
    
#     # root.deiconify() makes the state of root be "normal"
#     is_deiconify = root.state() == "normal"

#     all_assertions = {
#         "is_deiconify": is_deiconify
#     }

#     for key, assertion in all_assertions.items():
#         with subtests.test(msg=f"Asserting {key}"):
#             assert assertion

# # Tests are run by pytest in the order they are defined
# def helper_test_exit_key(test_env, subtests):

#     root, sw, sh, FONTS, COLORS, WINDOWS = test_env

#     # Test that Ctrl + D, then "a" properly turns off the overlay


#     # Check that the overlay was on before
#     is_deiconify_before = root.state() == "normal"

#     # Simulate A
#     key_simulator.press("a")
#     # Release A
#     key_simulator.release("a")

#     # The gui_queue logic polls the queue once every 100ms
#     # Thus wait for 150ms minimally to allow the gui_queue to catch the keypress
#     wait(root, 0.15) # 0.15s = 150ms

#     # Check that the overlay is withdrawn now
#     is_withdrawn = root.state() == "withdrawn"
#     print(root.state())
#     all_assertions = {
#         "is_deiconify_before": is_deiconify_before,
#         "is_withdrawn": is_withdrawn
#     }

#     for key, assertion in all_assertions.items():
#         with subtests.test(msg=f"Asserting {key}"):
#             assert assertion

# def helper_test_wrong_key(test_env, subtests):

#     root, sw, sh, FONTS, COLORS, WINDOWS = test_env

#     # Check that the screen properly goes red, then turns off when a wrong key is pressed after Ctrl + D

#     # Press Ctrl + D now
#     # Simulate Ctrl
#     key_simulator.press(keyboard.Key.ctrl_l)

#     # Simulate D while holding Ctrl down
#     key_simulator.press("d")

#     # Release both
#     key_simulator.release(keyboard.Key.ctrl_l)
#     key_simulator.release("d")
    
#     wait(root, 0.15)

#     # Check that the overlay was on before
#     is_deiconify_before = root.state() == "normal"
#     # print(root.state())

#     # Let the wrong keypress be F
#     # Simulate F
#     key_simulator.press("f")
#     # Release F
#     key_simulator.release("f")

#     # Wait 150ms to allow the gui_queue polling loop to catch it
#     wait(root, 0.15) # 0.15s = 150ms

#     # Overlay should be red now
#     canvas = root.nametowidget(".overlay")
#     is_red = canvas.itemcget("overlay", "outline") == "red"

#     # Red overlay is flashed for 1s
#     # Thus wait 1.05s to allow the red overlay to go away
#     wait(root, 1.05)

#     # Overlay should be withdrawn now
#     is_withdrawn = root.state() == "withdrawn"

#     all_assertions = {
#         "is_deiconify_before": is_deiconify_before,
#         "is_red": is_red,
#         "is_withdrawn": is_withdrawn
#     }

#     for key, assertion in all_assertions.items():
#         with subtests.test(msg=f"Asserting {key}"):
#             assert assertion
