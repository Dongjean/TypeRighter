import tkinter as tk
from tkinter import font as tkfont

import utils.latex as latex

canvas = None

# Compile the LaTeX code
def compile_latex_codecogs(canvas, text_editor):

    # Get all text minus the auto-added trailing newline
    latex_code = text_editor.get("1.0", "end-1c")

    latex.display_latex_window_codecogs(canvas, latex_code)

    return "break"

def build_latex_workspace(root, COLORS, FONTS):

    # Frame for LaTeX workspace
    latex_frame = tk.Frame(root, bg=COLORS["bg_main"], padx=20, pady=20, takefocus=True, name="latex_frame")
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
    preview_label = tk.Frame(latex_output_container, bg="white")
    preview_label.pack(fill="both", expand=True)

    # Initialise the latex window the moment the output frame is mounted
    global canvas
    canvas = latex.init_latex_window_codecogs(preview_label, "white")

    # LaTeX compiler button and key listener
    compile_button = tk.Button(editor_container, text="Compile", bg=COLORS["border"], fg=COLORS["text_main"], bd=0, relief="flat", font=FONTS["font_subtitle"], command=(lambda: compile_latex_codecogs(canvas, text_editor)))
    compile_button.pack(side="right")

    # Listen to Enter key anywhere
    root.bind("<Return>", lambda event: compile_latex_codecogs(canvas, text_editor))
    text_editor.bind("<Return>", lambda event: compile_latex_codecogs(canvas, text_editor))

    # Listen for Shift + Enter for breaklines
    root.bind("<Shift-Return>", lambda event: None)
    text_editor.bind("<Shift-Return>", lambda event: None)

# Destroy function to tear down latex workspace
def destroy_latex_workspace(root):

    # Remove all child widgets except for the navbar
    for widget in root.winfo_children():
        if widget.winfo_name() != "navbar_frame":
          widget.destroy()

    # Remove the latex-specific keybinds on root
    root.unbind("<Return>")
    root.unbind("<Shift-Return")