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

border_thickness = 5
key_simulator = keyboard.Controller() 

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

#Pytest automatically runs tests w/o argument passed manually
@pytest.fixture(scope="module", autouse = True)

#temp path for tests, avoid overwriting
#creates a temp file cleaned by OS later
#saves original bindings and directory
def isolate_binding(tmp_path_factory): 
    fake_dir = tmp_path_factory.mktemp("unicode_bindings")
    fake_path = str(fake_dir / "test_shortcuts_unicode.json")
    saved_path = shortcuts_unicode._PATH
    saved_bindings = dict(shortcuts_unicode.bindings)
    shortcuts_unicode._PATH = fake_path 
    shortcuts_unicode.bindings.clear() 

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
    root = main.root_view.root_init()
    root.update()


    # Start a completely new pynput thread
    # pynput threads cannot be reused
    listener = keyboard.Listener(on_press=lambda key: main.on_press(key, listener), on_release=lambda key: main.on_release(key, listener))
    main.COMBINATION = {
        listener.canonical(keyboard.Key.ctrl_l),
        keyboard.KeyCode.from_char('d'),
    }
    listener.start()

    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()

    # Custom Fonts
    FONTS = {
        "font_title": tkfont.Font(family="Segoe UI", size=16, weight="bold"),
        "font_subtitle": tkfont.Font(family="Segoe UI", size=10, weight="normal"),
        "font_hyperlink": tkfont.Font(family="Segoe UI", size=10, weight="normal", underline=True),
    }

    yield (root, sw, sh, FONTS)

        # Destroy the root window
    main.root_view.gui_queue.put("destroy_root")

    # Stop the pynput listener
    listener.stop()

    # Sleep for 150ms to let the tkinter root window properly close
    time.sleep(0.15)

    root.update()
    # Delete all .after() instances
    try:
        for after_id in root.eval('after info').split():
            print(after_id)
            root.after_cancel(after_id)
    except Exception as e:
        print(e)

    
#check if widget exists
def check_tk_exists(parent, child_name): 
    try: 
        child_widget = parent.nametowidget(child_name)
        return(child_widget, True) 
    
    #if child widget name does not exist
    except KeyError: 
        return(None, False)
    
    #if the parent widget does not exist
    except AttributeError: 
        return(None, False)
    

#check widget properties
def check_widget_props(widget, props):
    if widget is None: 
        return False
    
    widget_pack_info = None
    widget_binds = None
    try:
        widget_pack_info = widget.pack_info()
    except AttributeError as e:
        print(e)
    try:
        widget_binds = widget.bind()
    except AttributeError as e:
        print(e)
    curr_props = [

        # Command prop (Check that the function exists only)
        (prop[0], prop[1], True if widget.cget(prop[1]) else False) if prop[0] == "config" and prop[1] == "command"
        else
        # variable prop (for RadioButton)
        (prop[0], prop[1], str(widget.cget(prop[1]))) if prop[0] == "config" and prop[1] == "variable"
        else
        # Config props (config styles i.e. bg, text)
        (prop[0], prop[1], widget.cget(prop[1])) if prop[0] == "config"
        else
        # Pack props (config layouts)
        (prop[0], prop[1], widget_pack_info[prop[1]]) if prop[0] == "pack"
        else
        # Widget name prop
        (prop[0], prop[1], widget.winfo_name()) if prop[0] == "misc" and prop[1] == "widget_name"
        else
        # Font prop
        (prop[0], prop[1], tkfont.nametofont(widget.cget("font")).actual()) if prop[0] == "misc" and prop[1] == "font"
        else
        # pack_propagate prop
        (prop[0], prop[1], widget.tk.call('pack', 'propagate', widget._w)) if prop[0] == "misc" and prop[1] == "pack_propagate"
        else
        # Bind prop
        (prop[0], prop[1], prop[2] if prop[2] in widget_binds else None) if prop[0] == "misc" and prop[1] == "bind"
        else
        # Python syntax demands a fallback
        (prop[0], prop[1], prop[2])
        for prop in props
    ]
    print(curr_props)
    is_widget_props = all([
        curr_props[index] == prop for index, prop in enumerate(props)
    ])
    
    return is_widget_props

#check if unicode search menu opens
def get_unicode_menu_build_test(root, FONTS): 
    panel_frame, is_panel_frame = check_tk_exists(root, "unicode_search_panel")

    #for all widgets within the search frame w/o names
    children = panel_frame.winfo_children() if is_panel_frame else[]


    title_label = next( 
        (w for w in children if isinstance(w, tk.Label)and w.cget("text") == "Unicode Symbol Search"), 
        None,
    )

    subtitle_label = next(
        (w for w in children if isinstance(w, tk.Label) and w.cget("text") == "Search for unicode symbols by name or codepoint"),
        None,
    )
    search_box = next((w for w in children if isinstance(w, tk.Entry)), None)
    results_frame = next((w for w in children if isinstance(w, tk.Frame)), None)

    #check if search menu's inner widget exists (future: to name each inner widgets)
    is_title_label = title_label is not None
    is_subtitle_label = subtitle_label is not None
    is_search_box = search_box is not None
    is_results_frame = results_frame is not None

    #panel_frame
    panel_frame_props = [ 
        ("config", "bg", COLORS["bg_main"]), 
        ("config", "padx", 20), 
        ("config", "pady", 20), 
        ("config", "takefocus", "1"),

        ("pack","side", "top"),
        ("pack", "fill", "both"),
        ("pack", "expand", True),

        ("misc", "widget_name", "unicode_search_panel"),
    ] 
    is_panel_frame_props = check_widget_props(panel_frame, panel_frame_props)
   
    #title_label
    title_label_prop= [ 
        ("config", "bg", COLORS["bg_main"]),
        ("config", "fg", COLORS["text_main"]),
        ("misc", "font", FONTS["font_title"].actual()),
        ("config", "text", "Unicode Symbol Search"),
        ("pack", "fill", "x"),
        ("pack", "pady", 0),
    ]
    is_title_label_props = check_widget_props(title_label, title_label_prop)

    #subtitle_label 
    subtitle_label_prop = [ 
        ("config", "fg", COLORS["text_muted"]), 
        ("config", "bg", COLORS["bg_main"]),
        ("config", "text", "Search for unicode symbols by name or codepoint"),
        ("pack", "fill", "x"),
        ("pack", "pady", (0,15)),
        ("misc", "font", FONTS["font_subtitle"].actual()),
    ]

    is_subtitle_label_props = check_widget_props(subtitle_label, subtitle_label_prop)

    #search_box
    search_box_prop = [ 
        ("config", "fg", COLORS["text_main"]), 
        ("config", "bg", COLORS["bg_input"]),
        ("config", "insertbackground", "white"), 
        ("config", "highlightbackground", COLORS["border"]), 
        ("config", "highlightthickness", 1), 
        ("config", "bd", 1),
        ("pack", "fill", "x"),
        ("pack", "ipady", 6),
        ("misc", "font", FONTS["font_subtitle"].actual()),
    ]
    is_search_box_props=check_widget_props(search_box,search_box_prop)

    #results_frame 
    results_frame_prop = [ 
        ("config", "bg", COLORS["bg_main"]), 
        ("pack", "fill", "both"), 
        ("pack", "expand", True),
        ("pack", "pady", (15,0)), 
    ]
    is_result_frame_props = check_widget_props(results_frame,results_frame_prop)

    #verify the toggling from latex window to unicode window destorys the previous 
    _, is_latex_frame_present = check_tk_exists(root, "latex_frame")
    is_latex_frame_destroyed = not is_latex_frame_present

    return { 
        "is_panel_frame": is_panel_frame, 
        "is_title_label": is_title_label, 
        "is_subtitle_label": is_subtitle_label, 
        "is_search_box": is_search_box, 
        "is_results_frame": is_results_frame, 
        "is_panel_frame_prop": is_panel_frame_props,
        "is_title_label_prop": is_title_label_props, 
        "is_subtitle_label_prop": is_subtitle_label_props, 
        "is_search_box_prop": is_search_box_props, 
        "is_results_frame_prop": is_result_frame_props, 
        "is_latex_frame_destroyed": is_latex_frame_destroyed,
    }

def test_unicode_search_menu(test_env, subtests): 

    root, sw, sh, FONTS = test_env 
    # Check that the control panel properly opens, with the LaTeX editor as the default first window

    # Press Ctrl + D now
    # Simulate Ctrl
    key_simulator.press(keyboard.Key.ctrl_l)

    # Simulate D while holding Ctrl down
    key_simulator.press("d")

    # Release both
    key_simulator.release(keyboard.Key.ctrl_l)
    key_simulator.release("d")
    
    time.sleep(0.15)
    root.update()

    #enter control-panel-mode with\ 
    key_simulator.press("\\")
    key_simulator.release("\\")
    time.sleep(0.15)
    root.update()

    #finds unicode search button
    navbar_frame = root.nametowidget("navbar_frame")
    unicode_radio = navbar_frame.nametowidget("unicode-search")
    unicode_radio.invoke() #simulate pressing of unicode search on navigation bar
    root.update()

    #check that unicode search is indeed the curr window 
    is_unicode_selected = navbar_frame.selected_window.get() == "unicode-search" 

    unicode_setting_tests = get_unicode_menu_build_test(root, FONTS)

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
    root, sw, sh, FONTS = test_env

    shortcuts_unicode.bindings.clear()
    shortcuts_unicode.set_binding("q", "Ω")

    # The control panel is still open. 
    # Close it with Alt+F4 to return to overlay state.
    key_simulator.press(keyboard.Key.alt_l)
    key_simulator.press(keyboard.Key.f4)
    key_simulator.release(keyboard.Key.alt_l)
    key_simulator.release(keyboard.Key.f4)
    time.sleep(0.15)
    root.update()

    is_control_panel_closed = main.root_view.is_control_panel_open == False

    # Reset the clipboard to a known sentinel so we can detect change
    pyperclip.copy("Pray")

    # trigger overlay with Ctrl+D
    key_simulator.press(keyboard.Key.ctrl_l)
    key_simulator.press("d")
    key_simulator.release(keyboard.Key.ctrl_l)
    key_simulator.release("d")
    time.sleep(0.15)
    root.update()

    is_overlay_on_before = main.root_view.is_overlay_triggered == True

    key_simulator.press("q")
    key_simulator.release("q")
    time.sleep(0.15)
    root.update()

    is_clipboard_has_symbol = pyperclip.paste() == "Ω"
    is_overlay_off_after = main.root_view.is_overlay_triggered == False
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


