import tkinter as tk

import utils.latex as latex
import utils.shortcuts_unicode as shortcuts_unicode
import utils.scroll as scroll

canvas = None

# Compile the LaTeX code
def compile_latex_codecogs(canvas, text_editor):

    # Get all text minus the auto-added trailing newline
    latex_code = text_editor.get("1.0", "end-1c")

    latex.display_latex_window_codecogs(canvas, latex_code)
    latex.copy_canvas_image(canvas)

    return "break"

def download_latex(canvas):

    # Get the current image in the canvas
    latex_img = canvas.pil_img

    save_path = tk.filedialog.asksaveasfilename(
        initialfile="latex_output_TypeRighter",
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
    )

    latex_img.save(save_path)

def insert_latex_shortcut(editor_container, latex_code):
    text_editor = editor_container.nametowidget("text_editor")

    if text_editor:
        text_editor.focus_set()
        text_editor.insert(tk.INSERT, latex_code)

def build_latex_workspace(root, COLORS, FONTS):

    # Frame for LaTeX workspace
    latex_frame = tk.Frame(root, bg=COLORS["bg_main"], padx=20, pady=20, takefocus=True, name="latex_frame")
    latex_frame.pack(side="top", fill="both", expand=True)

    latex_frame = scroll.ScrollableFrame(root, bg=COLORS["bg_main"], padx=20, pady=20, takefocus=True, name="latex_frame")
    latex_frame.pack(side="top", fill="both", expand=True)

    # Header Titles
    # Set to be at the top, centred (expand=False by default)
    title_label = tk.Label(latex_frame.scrollable_frame, text="LaTeX Equation Editor", fg=COLORS["text_main"], bg=COLORS["bg_main"], font=FONTS["font_title"], name="title_label")
    title_label.pack(fill="x", pady=0)
    
    subtitle_label = tk.Label(latex_frame.scrollable_frame, text="Edit and preview complex mathematical formulas", fg=COLORS["text_muted"], bg=COLORS["bg_main"], font=FONTS["font_subtitle"], name="subtitle_label")
    subtitle_label.pack(fill="x", pady=(0, 15))

    # Editor Container (LaTeX input text)
    editor_container = tk.Frame(latex_frame.scrollable_frame, bg=COLORS["bg_main"], bd=0, name="editor_container")
    editor_container.pack(fill="both", expand=True)

    # LaTeX Shortcuts Container
    latex_shortcuts_container = tk.Frame(editor_container, bg=COLORS["bg_main"], name="latex_shortcuts_container")
    latex_shortcuts_container.pack()

    # # Fake list of LaTeX Shortcuts
    # LATEX_SHORTCUTS = {
    #     "frac_shortcut": {"name": "Fraction", "code": r"\frac{a}{b}"},
    #     "matrix_shortcut_1": {"name": "3x3 Identity Matrix", "code": r"\begin{pmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{pmatrix}"},
    # }

    LATEX_SHORTCUTS = shortcuts_unicode.all_latex_shortcuts()

    # Buttons for inserting LaTeX Shortcuts
    for key, shortcut in LATEX_SHORTCUTS.items():
        latex_shortcut = tk.Button(latex_shortcuts_container, text=shortcut["name"], relief="flat", activebackground=COLORS["accent_blue"], fg=COLORS["text_main"], bg=COLORS["border"], bd=1, highlightbackground=COLORS["border"], highlightthickness=1, font=FONTS["font_subtitle"], takefocus=False, command=lambda shortcut=shortcut: insert_latex_shortcut(editor_container, shortcut["code"]), name=f"{key}_latex_shortcut")
        latex_shortcut.pack(side="left", padx=5, pady=(0, 10))

    text_editor = tk.Text(editor_container, height=5, bg=COLORS["bg_input"], fg=COLORS["text_main"], insertbackground="white", bd=1, highlightbackground=COLORS["border"], highlightthickness=1, font=FONTS["font_subtitle"], padx=15, pady=15, wrap="none", name="text_editor")
    text_editor.pack(fill="both", expand=True)

    # LaTeX Output Container
    latex_output_container = tk.Frame(latex_frame.scrollable_frame, bg=COLORS["bg_input"], bd=1, highlightbackground=COLORS["border"], highlightthickness=1, height=150, name="latex_output_container")
    latex_output_container.pack(fill="x", pady=(5, 20))
    # Fix the height of the LaTeX Output Container
    latex_output_container.pack_propagate(False)

    # LaTeX Image Output
    preview_label = tk.Frame(latex_output_container, bg="white", name="preview_label")
    preview_label.pack(fill="both", expand=True)

    # LaTeX download button
    download_button = tk.Button(preview_label, text="Download", bg=COLORS["border"], fg=COLORS["text_main"], bd=0, relief="flat", font=FONTS["font_subtitle"], command=(lambda: download_latex(canvas)), name="download_button")
    download_button.place(in_=preview_label, relx=1, rely=1, anchor="se")

    # Initialise the latex window the moment the output frame is mounted
    global canvas
    canvas = latex.init_latex_window_codecogs(preview_label, "white")

    # LaTeX compiler button
    compile_button = tk.Button(editor_container, text="Compile", bg=COLORS["border"], fg=COLORS["text_main"], bd=0, relief="flat", font=FONTS["font_subtitle"], command=(lambda: compile_latex_codecogs(canvas, text_editor)), name="compile_button")
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