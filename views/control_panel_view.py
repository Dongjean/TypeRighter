from tkinter import font as tkfont
import sys

import components.navbar as navbar

def control_panel_init(root):
    
    textbox = root.nametowidget("textbox")
    textbox.destroy()
    root.title("TypeRighter - Control Panel")

    # Manually reset all of the settings from root_init()
    root.overrideredirect(False)
    root.attributes("-topmost", False)
    root.attributes("-alpha", 1.0)
    if sys.platform.startswith("win"):
        root.attributes("-transparentcolor", "") # Clear the transparent color mask

    # Get the canvas and delete it
    canvas = root.children["overlay"]
    canvas.destroy()
    
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    root.geometry(f"{sw // 2}x{sh // 2}+0+0")
    root.configure(bg="#ffffff")

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

    # Custom Fonts
    FONTS = {
        "font_title": tkfont.Font(family="Segoe UI", size=16, weight="bold"),
        "font_subtitle": tkfont.Font(family="Segoe UI", size=10, weight="normal"),
        "font_hyperlink": tkfont.Font(family="Segoe UI", size=10, weight="normal", underline=True),
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
        "AI Assistant":{
            "name": "AI Assistant", 
            "icon":"",
        },
        "settings-window": {
            "name": "Settings",
            "icon": "",
        },
    }

    # Build the navbar and initialise the first window
    navbar.build_navbar(root=root, COLORS=COLORS, FONTS=FONTS, WINDOWS=WINDOWS, start_window="latex-workspace")
    
    # Clicking anywhere in the control panel brings active focus to there
    root.bind("<Button-1>", lambda event: event.widget.focus_set())

    root.update_idletasks()
    root.focus_force()