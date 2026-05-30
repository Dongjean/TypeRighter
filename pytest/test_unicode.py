import pytest 
import tkinter 
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
def test_env():

#temp path for tests, avoid overwriting
#creates a temp file cleaned by OS later
#saves original bindings and directory
    def isolate_binding(temp_path_factory): 
        fake_dir = temp_path_factory.mktemp("unicode_bindings")
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


def 