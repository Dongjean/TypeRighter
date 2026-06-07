import pytest
from tkinter import font as tkfont

import main as main
from pynput import keyboard
import utils.shortcuts_unicode as shortcuts_unicode

# Import helper functions
from helper_functions.main_test_helpers import wait
from tester_functions.main_testers import overlay_tester, latex_tester,navbar_tester, unicode_tester

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

@pytest.fixture(scope="module")
def test_env():

    # This part runs before the test_ functions
    # Initialise the tkinter root window and the pynput listener

    # Manually initialize the tkinter window without .mainloop()
    # Run root_view.root_init() without the last root.mainloop() line

    # Start the pynput thread
    # main.listener.start()

    listener = keyboard.Listener(on_press=lambda key: main.on_press_bg(key, listener), on_release=lambda key: main.on_release_bg(key, listener))
    listener.start()

    root = main.view_handler.root_init()
    root.update()
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

    yield (root, sw, sh, FONTS, COLORS, WINDOWS) # This is where the code runs

    # This is after all the tests
    # Close everything
    
    # Destroy the root window
    main.view_handler.gui_queue.put("destroy_root")

    # Stop the pynput listener
    # main.listener.stop()
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

def test_systematic(test_env, subtests):

    overlay_tester(test_env, subtests)

    latex_tester(test_env, subtests)

    navbar_tester(test_env, subtests)

    unicode_tester(test_env, subtests)