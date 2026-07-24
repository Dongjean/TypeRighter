import pytest
from tkinter import font as tkfont
import pystray
from PIL import Image
from pathlib import Path
import shutil
import os

import main as main
from pynput import keyboard
import utils.shortcuts_unicode as shortcuts_unicode
import views.view_handler as view_handler

# Import helper functions
from helper_functions.main_test_helpers import wait
from tester_functions.main_testers import bg_listener_tester, overlay_tester

key_simulator = keyboard.Controller()

@pytest.fixture(scope="module", autouse=True)
def systematic_test_env(tmp_path_factory):

    # This part runs before the test_ functions

    # Move all the files and folders in APPDATA/TypeRighter in a temporary folder
    source_path = Path(shortcuts_unicode._data_dir()).resolve()
    destination_path = tmp_path_factory.mktemp("pytest_temp")

    for item in source_path.iterdir():
        target = destination_path / item.name

        if target.exists():
            raise FileExistsError(f"Destination already contains: {target}")

        shutil.move(str(item), str(target))

    # Initialise the tkinter root window, pynput listener and runtime variables

    # Manually initialize the tkinter window without .mainloop()
    # Run root_view.root_init() without the last root.mainloop() line

    shortcuts_unicode.load()

    main.BREAKOUT_KEY = shortcuts_unicode.get_key_from_value("Breakout Key") or "\\"
    main.COMBINATION = [
        keyboard.Key.ctrl_l,
        keyboard.Key.alt_l,
        keyboard.Key.space
    ]

    # We are going to use this one binding at the start of our systematic tests
    shortcuts_unicode.bindings["unicode"]["q"] = "∃"

    # Start the pynput BG Listener Thread
    bg_listener = keyboard.Listener(on_press=lambda key: main.on_press_bg(key, bg_listener), on_release=lambda key: main.on_release_bg(key, bg_listener))
    bg_listener.start()

    # Start the Tray Icon
    icon = pystray.Icon("TypeRighter")
    icon.icon = main.create_image()
    icon.menu = pystray.Menu(
        pystray.MenuItem("Run Now", lambda icon, item: main.trigger_overlay()),
        pystray.MenuItem("Exit", lambda icon, item: main.clean_exit())
    )
    icon.run_detached()

    view_handler.icon = icon

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
        "action_green": "#00FF00",
        "error_red": "#FF0000",
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
        },
        "settings-window": {
            "name": "Settings",
            "icon": "",
        },
    }

    yield (root, sw, sh, FONTS, COLORS, WINDOWS) # This is where the code runs

    # This is after all the tests
    # Close everything

    # Bring back the files and folders from the temporary folder
    for item in source_path.iterdir():
        target = source_path / item.name
        if os.path.isdir(target):
            shutil.rmtree(target)  # Deletes folder
        else:
            os.remove(target)
    
    for item in destination_path.iterdir():
        target = source_path / item.name

        if target.exists():
            raise FileExistsError(f"Destination already contains: {target}")

        shutil.move(str(item), str(target))

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
            root.after_cancel(after_id)
    except Exception as e:
        print(e)

    main.clean_exit()

def test_systematic(systematic_test_env, subtests):

    bg_listener_tester(systematic_test_env, subtests)
    
    overlay_tester(systematic_test_env, subtests)
    
    # Previous tester functions (keeping for reference)
    # latex_tester(test_env, subtests)

    # navbar_tester(test_env, subtests)

    # unicode_tester(test_env, subtests)