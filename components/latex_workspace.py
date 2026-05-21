import tkinter as tk
from tkinter import font as tkfont

def build_latex_workspace(root, COLORS, FONTS):

    # Frame for LaTeX workspace
    latex_frame = tk.Frame(root, bg=COLORS["bg_main"], padx=20, pady=20)
    latex_frame.pack(side="top", fill="both", expand=True)

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

    # LaTeX Output Container
    latex_output_container = tk.Frame(latex_frame, bg=COLORS["bg_input"], bd=1, highlightbackground=COLORS["border"], highlightthickness=1, height=150)
    latex_output_container.pack(fill=tk.X, pady=(5, 20))
    # Fix the height of the LaTeX Output Container
    latex_output_container.pack_propagate(False)

    # LaTeX Image Output (incomplete)
    preview_label = tk.Label(latex_output_container, text="OUR fake... latex output (incomplete)", fg=COLORS["text_main"], bg=COLORS["bg_input"], font=FONTS["font_subtitle"])
    preview_label.pack(expand=True)