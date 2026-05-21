import tkinter as tk
from tkinter import font as tkfont

import components.latex_workspace as latex_workspace

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
    }

    # Custom Fonts
    FONTS = {
        "font_title": tkfont.Font(family="Segoe UI", size=16, weight="bold"),
        "font_subtitle": tkfont.Font(family="Segoe UI", size=10, weight="normal"),
    }

    latex_workspace.build_latex_workspace(root=root, COLORS=COLORS, FONTS=FONTS)

    root.update_idletasks()
    root.focus_force()