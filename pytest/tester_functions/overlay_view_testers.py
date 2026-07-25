import sys
from pynput import keyboard
import pyperclip
import utils.shortcuts_unicode as shortcuts_unicode
import utils.templates as templates
import utils.settings as settings

key_simulator = keyboard.Controller()

from tester_functions.bg_listener_testers import helper_test_bg_listener_on, helper_test_bg_listener_off

from helper_functions.main_test_helpers import wait, check_tk_exists
from helper_functions.overlay_view_test_helpers import get_overlay_init_tests

import main as main

border_thickness = 5

def helper_test_overlay_breakout_key_on(test_env, subtests):
    
    root, sw, sh, FONTS, COLORS, WINDOWS = test_env
    
    key_simulator.press(keyboard.KeyCode.from_char('\\'))


    # with key_simulator.pressed("\\"):
    #     wait(root, 0.5)
    #     key_simulator.press("a")
    #     key_simulator.release("a")
    #     wait(root, 1)
    
    # wait(root, 0.5)

    # key_simulator.press("a")
    # key_simulator.release("a")

    # key_simulator.release(keyboard.KeyCode.from_char('\\'))

    wait(root, 0.5)

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

    wait(root, 0.5)

    command_textbox, is_command_textbox = check_tk_exists(root, "textbox")

    # Test command popup if its closed
    # If we are opening Control Panel, the command textbox will no longer exist
    if is_command_textbox:
        is_withdrawn = command_textbox.state() == "withdrawn"

        all_assertions = {
            "is_withdrawn": is_withdrawn
        }
        
        for key, assertion in all_assertions.items():
            with subtests.test(msg=f"Asserting {key}"):
                assert assertion

def helper_test_overlay_unicode_shortcut(test_env, subtests):

    root, sw, sh, FONTS, COLORS, WINDOWS = test_env
    
    helper_test_overlay_breakout_key_on(test_env, subtests)
    
    # In the systematic test environment, q is mapped to ∃
    key_simulator.press("q")

    wait(root, 0.5)

    command_textbox, is_command_textbox = check_tk_exists(root, "textbox")
    command_prompt, is_command_prompt = check_tk_exists(command_textbox, "typed")
    command_preview, is_command_preview = check_tk_exists(command_textbox, "preview")

    is_command_displayed = command_prompt.cget("text") == "q" # Typed command display is correct
    is_command_color = command_prompt.cget("fg") == "white" # Typed command display is white, not red
    is_preview = command_preview.cget("text") == "∃" # Command preview is properly displaying

    # Release breakout key and check that ∃ is typed and copied
    helper_test_overlay_breakout_key_off(test_env, subtests)

    # Checks if unicode is copied
    is_unicode_copied = pyperclip.paste() == "∃"
    
    # Check if unicode is typed (TODO)

    all_assertions = {
        "is_command_displayed": is_command_displayed,
        "is_command_color": is_command_color,
        "is_preview": is_preview,
        "is_unicode_copied": is_unicode_copied
    }

    for key, assertion in all_assertions.items():
        with subtests.test(msg=f"Asserting {key}"):
            assert assertion

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
