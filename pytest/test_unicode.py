import pytest 
import tkinter as tk
from tkinter import font as tkfont
import sys 
import main as main 
import time 
from pynput import keyboard 
import pyperclip 
import utils.unicode_search as unicode_search 
import utils.shortcuts_unicode as shortcuts_unicode

# Import helper functions
from helpers.main_test_helpers import wait
from helpers.unicode_window_test_helpers import get_unicode_menu_build_test

border_thickness = 5
key_simulator = keyboard.Controller()

#Pytest automatically runs tests w/o argument passed manually
@pytest.fixture(scope="module", autouse = True)

#temp path for tests, avoid overwriting
#creates a temp file cleaned by OS later
#saves original bindings and directory
def isolate_binding(tmp_path_factory): 
    print("1")
    fake_dir = tmp_path_factory.mktemp("unicode_bindings")
    print("2")
    fake_path = str(fake_dir / "test_shortcuts_unicode.json")
    print("3")
    saved_path = shortcuts_unicode._PATH
    print("4")
    saved_bindings = dict(shortcuts_unicode.bindings)
    print("5")
    shortcuts_unicode._PATH = fake_path 
    print("6")
    shortcuts_unicode.bindings.clear() 
    print("7")
    yield 

    #load saved bindings and actual directory 
    shortcuts_unicode._PATH = saved_path 
    shortcuts_unicode.bindings.clear()
    shortcuts_unicode.bindings.update(saved_bindings)
       
@pytest.fixture(scope = "module")
def test_env(): 

    # This part runs before the test_ functions

    # Initialise the tkinter root window and the pynput listener
    # Manually initialize the tkinter window without .mainloop()
    # Run root_view.root_init()
    root = main.view_handler.root_init()
    root.update()


    # Start a completely new pynput thread
    # pynput threads cannot be reused
    listener = keyboard.Listener(on_press=lambda key: main.on_press_bg(key, listener), on_release=lambda key: main.on_release_bg(key, listener))
    listener.start()

    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()

    # Custom Fonts
    FONTS = {
        "font_title": tkfont.Font(family="Segoe UI", size=16, weight="bold"),
        "font_subtitle": tkfont.Font(family="Segoe UI", size=10, weight="normal"),
        "font_hyperlink": tkfont.Font(family="Segoe UI", size=10, weight="normal", underline=True),
    }

    # Color Palette
    COLORS = {
        "bg_main": "#202020",
        "bg_input": "#1a1a1a",
        "text_main": "#e3e3e3",
        "text_muted": "#888888",
        "border": "#2d2d2d",
        "accent_blue": "#2a5a9c",
        "hyperlink_blue": "#0099FF",
        "action_green":"#00FF00"
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
        }, 
        "unicode-search": { 
        "name": "Unicode\nSearch",
        "icon": "",
        }
    }
    
    yield (root, sw, sh, FONTS, COLORS, WINDOWS)

    # Destroy the root window
    main.view_handler.gui_queue.put("destroy_root")

    # Stop the pynput listener
    main.stop_all_pynput_keyboard_listeners()

    # Sleep for 150ms to let the tkinter root window properly close
    wait(root, 0.15)

    # Delete all .after() instances
    try:
        for after_id in root.eval('after info').split():
            print(after_id)
            root.after_cancel(after_id)
    except Exception as e:
        print(e)  

def test_unicode_search_menu(test_env, subtests):

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

    #enter control-panel-mode with\ 
    key_simulator.press("\\")
    key_simulator.release("\\")
    wait(root, 0.15)

    #finds unicode search button
    navbar_frame = root.nametowidget("navbar_frame")
    unicode_radio = navbar_frame.nametowidget("unicode-search")
    unicode_radio.invoke() #simulate pressing of unicode search on navigation bar
    root.update()

    #check that unicode search is indeed the curr window 
    is_unicode_selected = navbar_frame.selected_window.get() == "unicode-search" 

    unicode_setting_tests = get_unicode_menu_build_test(root, FONTS, COLORS, WINDOWS)

    all_assertions = { 
        "is_unicode_selected": is_unicode_selected, 
        **unicode_setting_tests, 
    }

    for key, assertion in all_assertions.items():
        with subtests.test(msg=f"Asserting {key}"):
            assert assertion

def test_unicode_search_function(subtests): 

    #search by codepoint

    #search by cp with U+XXXX
    result_u = unicode_search.search_by_codepoint("U+03A9")
    is_codepoint_prefix_uplus = ( 
        result_u is not None
        and result_u[0] == "Ω"
        and result_u[1] == "GREEK CAPITAL LETTER OMEGA"
        and result_u[2] == 0x03A9
    )

    #search by cp with 0XXXXX
    result_0x = unicode_search.search_by_codepoint("0x03A9")
    is_codepoint_prefix_0x= ( 
        result_0x is not None
        and result_0x[0] == "Ω"
        and result_0x[1] == "GREEK CAPITAL LETTER OMEGA"
        and result_0x[2] == 0x03A9
    )

    #search by cp witout U+ (hex)
    result_bare_hex = unicode_search.search_by_codepoint("03A9")
    is_codepoint_prefix_bare_hex = (
        result_bare_hex is not None 
        and result_bare_hex[0] == "Ω"
        and result_bare_hex[1] == "GREEK CAPITAL LETTER OMEGA"
        and result_bare_hex[2] == 0x03A9
    )

    #search by cp without U+ (dec)
    result_bare_dec = unicode_search.search_by_codepoint("937")
    is_codepoint_prefix_bare_dec = ( 
        result_bare_dec is not None 
        and result_bare_dec[0] == "Ω"
        and result_bare_dec[1] == "GREEK CAPITAL LETTER OMEGA"
        and result_bare_dec[2] == 0x03A9
    )

    #search by cp HTML input 
    result_HTML = unicode_search.search_by_codepoint("&#937;")
    is_codepoint_HTML = (
        result_HTML is not None
        and result_HTML[0] == "Ω"
        and result_HTML[1] == "GREEK CAPITAL LETTER OMEGA"
        and result_HTML[2] == 0x03A9
    )

    #invalid input 
    is_codepoint_invalid = unicode_search.search_by_codepoint("not-hex") is None

    #search by name 
    result_name = unicode_search.search_by_name("GREEK CAPITAL LETTER OMEGA")
    is_name_found = any(ch == "Ω" for ch, _, _ in result_name)

    is_name_empty = unicode_search.search_by_name("") ==[]
    is_name_whitespace = unicode_search.search_by_name ("  ") == []

    result_limit_cap = unicode_search.search_by_name("LATIN", limit =5)
    is_result_limit_cap = len(result_limit_cap) <= 5

    #check binding to symbols
    check_bind, _ = shortcuts_unicode.set_binding("p", "Ω")
    is_bind_sucessful = check_bind and shortcuts_unicode.lookup("p") == "Ω"

    is_check_caps_insensitive_lookup = shortcuts_unicode.lookup("P") == "Ω"

    check_reserved, _ = shortcuts_unicode.set_binding("a", "Ω")
    is_reserved_key_blocked_successful = (not check_reserved) and (shortcuts_unicode.lookup("a") is None )

    check_empty , _ = shortcuts_unicode.set_binding("e", "")
    is_empty_blocked_successful = (not check_empty) and (shortcuts_unicode.lookup("e") is None)

    #check if bindings are stored 
    all_bindings_saved = shortcuts_unicode.all_bindings()
    is_all_bindings_correct = (all_bindings_saved.get("p") == "Ω" and "a" not in all_bindings_saved)

    is_remove = shortcuts_unicode.remove_binding("p") is True 
    is_remove_successful = shortcuts_unicode.lookup("p") is None 

    shortcuts_unicode.bindings.clear()

    all_assertions = {
        "is_codepoint_prefix_uplus": is_codepoint_prefix_uplus,
        "is_codepoint_prefix_0x": is_codepoint_prefix_0x,
        "is_codepoint_HTML": is_codepoint_HTML, 
        "is_codepoint_prefix_bare_hex": is_codepoint_prefix_bare_hex,
        "is_codepoint_prefix_bare_dec": is_codepoint_prefix_bare_dec,
        "is_codepoint_invalid": is_codepoint_invalid,
        
        "is_name_found": is_name_found,
        "is_name_empty": is_name_empty,
        "is_name_whitespace": is_name_whitespace,
        "is_result_limit_cap":is_result_limit_cap,
        "is_check_caps_insensitive_lookup":is_check_caps_insensitive_lookup,

        "is_empty_blocked_successful":is_empty_blocked_successful,
        "is_bind_sucessful":is_bind_sucessful,
        "is_reserved_key_blocked_successful":is_reserved_key_blocked_successful,
        "is_all_bindings_correct":is_all_bindings_correct,
        "is_remove":is_remove,
        "is_remove_successful":is_remove_successful
    } 
    for key, assertion in all_assertions.items():
        with subtests.test(msg=f"Asserting {key}"):
            assert assertion

    #check copy and paste function
def test_unicode_copy_paste (subtests):

    shortcuts_unicode.bindings.clear()

    #copy to clipboard 
    is_copy_successful= shortcuts_unicode.copy_to_clipboard("Ω") is True 
    is_match_copy_paste = pyperclip.paste() == "Ω"

    #empty input rejected
    is_empty_rejected = shortcuts_unicode.copy_to_clipboard("") is False

    #check copied symbol is the same as the symbol in cliperboard
    shortcuts_unicode.set_binding("s", "Ω")
    returned = shortcuts_unicode.copy_symbol("s")
    is_copied_symbol = returned == "Ω"
    is_match_copied_symbol_clipboard = pyperclip.paste() == "Ω"

    #check symbol on a unbound key 
    pyperclip.copy("Pray")
    is_unknown_return_none = shortcuts_unicode.copy_symbol("Nah") is None 
    is_unknown_clipboard_unchanged = pyperclip.paste() == "Pray"

    shortcuts_unicode.bindings.clear()

    all_assertions = { 
        "is_copy_successful":is_copy_successful,
        "is_match_copy_paste":is_match_copy_paste,
        "is_empty_rejected":is_empty_rejected,
        "is_copied_symbol": is_copied_symbol,
        "is_match_copied_symbol_clipboard": is_match_copied_symbol_clipboard,
        "is_unknown_return_none":is_unknown_return_none,
        "is_unknown_clipboard_unchanged": is_unknown_clipboard_unchanged,
    }
    
    for key, assertion in all_assertions.items():
        with subtests.test(msg=f"Asserting {key}"):
            assert assertion

def test_unicode_copy_via_overlay(test_env, subtests): 

    root, sw, sh, FONTS, COLORS, WINDOWS = test_env

    shortcuts_unicode.bindings.clear()
    shortcuts_unicode.set_binding("q", "Ω")

    # The control panel is still open. 
    # Close it with Alt+F4 to return to overlay state.
    key_simulator.press(keyboard.Key.alt_l)
    key_simulator.press(keyboard.Key.f4)
    key_simulator.release(keyboard.Key.alt_l)
    key_simulator.release(keyboard.Key.f4)
    wait(root, 0.15)

    is_control_panel_closed = main.view_handler.is_control_panel_open == False

    # Reset the clipboard to a known sentinel so we can detect change
    pyperclip.copy("Pray")

    # trigger overlay with Ctrl+D
    key_simulator.press(keyboard.Key.ctrl_l)
    key_simulator.press("d")
    key_simulator.release(keyboard.Key.ctrl_l)
    key_simulator.release("d")
    wait(root, 0.15)

    is_overlay_on_before = main.view_handler.is_overlay_triggered == True

    key_simulator.press("q")
    key_simulator.release("q")
    wait(root, 0.15)

    is_clipboard_has_symbol = pyperclip.paste() == "Ω"
    is_overlay_off_after = main.view_handler.is_overlay_triggered == False
    is_root_withdrawn = root.state() == "withdrawn"

    shortcuts_unicode.bindings.clear()

    all_assertions = {
        "is_control_panel_closed": is_control_panel_closed,
        "is_overlay_on_before": is_overlay_on_before,
        "is_clipboard_has_symbol": is_clipboard_has_symbol,
        "is_overlay_off_after": is_overlay_off_after,
        "is_root_withdrawn": is_root_withdrawn,
    }

    for key, assertion in all_assertions.items():
        with subtests.test(msg=f"Asserting {key}"):
            assert assertion