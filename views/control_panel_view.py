from tkinter import font as tkfont

import components.navbar as navbar

def control_panel_init(root):
    root.title("TypeRighter - Control Panel")

    # Manually reset all of the settings from root_init()
    root.overrideredirect(False)
    root.attributes("-topmost", False)
    root.attributes("-alpha", 1.0)
    root.attributes("-transparentcolor", "") # Clear the transparent color mask

    # Get the canvas and delete it
    canvas = root.children["overlay"]
    canvas.destroy()

    root.geometry("1050x720")
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
        }
    }

    # Build the navbar and initialise the first window
    navbar.build_navbar(root=root, COLORS=COLORS, FONTS=FONTS, WINDOWS=WINDOWS, start_window="latex-workspace")
    
    # Clicking anywhere in the control panel brings active focus to there
    root.bind("<Button-1>", lambda event: event.widget.focus_set())

    root.update_idletasks()
    root.focus_force()