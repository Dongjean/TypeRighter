import tkinter as tk
from tkinter import font as tkfont

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

    # Frame for LaTeX workspace
    latex_frame = tk.Frame(root, bg=COLORS["bg_main"], padx=20, pady=20)
    latex_frame.pack(side="top", fill="both", expand=True)

    build_latex_workspace(latex_frame=latex_frame, COLORS=COLORS, FONTS=FONTS)

    root.update_idletasks()
    root.focus_force()


def build_latex_workspace(latex_frame, COLORS, FONTS):
    # Header Titles
    # Set to be at the top, centred (expand=False by default)
    title_label = tk.Label(latex_frame, text="LaTeX Equation Editor", fg=COLORS["text_main"], bg=COLORS["bg_main"], font=FONTS["font_title"])
    title_label.pack(fill="x", pady=0)
    
    subtitle_label = tk.Label(latex_frame, text="Edit and preview complex mathematical formulas", fg=COLORS["text_muted"], bg=COLORS["bg_main"], font=FONTS["font_subtitle"])
    subtitle_label.pack(fill="x", pady=(0, 15))

    # Editor Container (LaTeX input text)
    editor_container = tk.Frame(latex_frame, bg=COLORS["bg_input"], bd=1, highlightbackground=COLORS["border"], highlightthickness=1)
    editor_container.pack(fill="both", expand=True)

    text_editor = tk.Text(editor_container, bg=COLORS["bg_input"], fg=COLORS["text_main"], insertbackground="white", bd=0, font=FONTS["font_subtitle"], padx=15, pady=15, wrap="none")
    text_editor.pack(fill="both", expand=True)