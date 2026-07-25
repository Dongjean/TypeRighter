from pynput import keyboard

key_simulator = keyboard.Controller()

import tkinter as tk
import pyperclip 
from helper_functions.main_test_helpers import wait, check_tk_exists, check_widget_props
import utils.unicode_search as unicode_search 
import utils.shortcuts_unicode as shortcuts_unicode
import main as main

from helper_functions.unicode_window_test_helpers import get_unicode_menu_build_test

def helper_test_unicode_search_menu(test_env, subtests):

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

    unicode_setting_tests = get_unicode_menu_build_test(root, FONTS, COLORS)

    all_assertions = { 
        "is_unicode_selected": is_unicode_selected, 
        **unicode_setting_tests, 
    }

    for key, assertion in all_assertions.items():
        with subtests.test(msg=f"Asserting {key}"):
            assert assertion

def helper_test_unicode_search_function(subtests): 

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
    check_bind, _ = shortcuts_unicode.set_unicode_binding("p", "Ω")
    is_bind_sucessful = check_bind and shortcuts_unicode.lookup_unicode("p") == "Ω"

    is_check_caps_insensitive_lookup = shortcuts_unicode.lookup_unicode("P") == "Ω"

    check_protected, _ = shortcuts_unicode.check_binding("s", "Ω")
    is_protected_key_blocked_successful = (check_protected == "protected") and (shortcuts_unicode.lookup_unicode("s") in shortcuts_unicode.PROTECTED_BINDS)

    check_empty , _ = shortcuts_unicode.set_unicode_binding("e", "")
    is_empty_blocked_successful = (not check_empty) and (shortcuts_unicode.lookup_unicode("e") is None)

    #check if unicode bindings are stored 
    all_unicode_bindings_saved = shortcuts_unicode.all_unicode_bindings()
    is_all_unicode_bindings_correct = (all_unicode_bindings_saved.get("p") == "Ω" and all_unicode_bindings_saved.get("q") == "∃" and shortcuts_unicode.DEFAULT_BINDINGS["unicode"].items() <= all_unicode_bindings_saved.items())
    
    #check if latex shortcuts are stored 
    all_latex_shortcuts_saved = shortcuts_unicode.all_latex_shortcuts()
    is_all_latex_shortcuts_correct = (shortcuts_unicode.DEFAULT_BINDINGS["latex"].items() <= all_latex_shortcuts_saved.items())

    is_remove = shortcuts_unicode.remove_unicode_binding("p") is True 
    is_remove_successful = shortcuts_unicode.lookup_unicode("p") is None 

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
        "is_protected_key_blocked_successful":is_protected_key_blocked_successful,
        "is_all_unicode_bindings_correct":is_all_unicode_bindings_correct,
        "is_all_latex_shortcuts_correct": is_all_latex_shortcuts_correct,
        "is_remove":is_remove,
        "is_remove_successful":is_remove_successful
    } 
    for key, assertion in all_assertions.items():
        with subtests.test(msg=f"Asserting {key}"):
            assert assertion

#check copy and paste function
def helper_test_unicode_copy_paste (subtests):

    shortcuts_unicode.bindings.clear()

    #copy to clipboard 
    is_copy_successful= shortcuts_unicode.copy_to_clipboard("Ω") is True 
    is_match_copy_paste = pyperclip.paste() == "Ω"

    #empty input rejected
    is_empty_rejected = shortcuts_unicode.copy_to_clipboard("") is False

    #check copied symbol is the same as the symbol in cliperboard
    shortcuts_unicode.set_unicode_binding("s", "Ω")
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