import tkinter as tk
from tkinter import font as tkfont

curr_window = ""

def change_window(selected_window):
    global curr_window
    if selected_window != curr_window:
        print(selected_window)
        curr_window = selected_window

def build_navbar(root, COLORS, FONTS, WINDOWS, start_window):

    # Frame for navbar
    navbar_frame = tk.Frame(root, bg=COLORS["bg_main"], takefocus=True)
    navbar_frame.pack(side="right", fill="both")

    # Display each window as a custom button
    navbar_frame.selected_window = tk.StringVar(value=start_window)
    curr_window = start_window
    for key, value in WINDOWS.items():
        btn = tk.Radiobutton(navbar_frame, text=value["name"], variable=navbar_frame.selected_window, value=key, bg=COLORS["border"], fg=COLORS["text_main"], bd=0, relief="flat", width=10, height=3, font=FONTS["font_subtitle"], selectcolor=COLORS["accent_blue"], activebackground=COLORS["accent_blue"], indicatoron=False, command=(lambda: change_window(navbar_frame.selected_window.get())))
        btn.pack(side="top")



    # Header Titles
    # Set to be at the top, centred (expand=False by default)
    # title_label = tk.Label(navbar_frame, text="LaTeX Equation Editor", fg=COLORS["text_main"], bg=COLORS["bg_main"], font=FONTS["font_title"])
    # title_label.pack(fill="x", pady=0)
    
    # subtitle_label = tk.Label(latex_frame, text="Edit and preview complex mathematical formulas", fg=COLORS["text_muted"], bg=COLORS["bg_main"], font=FONTS["font_subtitle"])
    # subtitle_label.pack(fill="x", pady=(0, 15))

    # # Editor Container (LaTeX input text)
    # editor_container = tk.Frame(latex_frame, bg=COLORS["bg_input"], bd=1, highlightbackground=COLORS["border"], highlightthickness=1)
    # editor_container.pack(fill="both", expand=True)

    # text_editor = tk.Text(editor_container, bg=COLORS["bg_input"], fg=COLORS["text_main"], insertbackground="white", bd=0, font=FONTS["font_subtitle"], padx=15, pady=15, wrap="none")
    # text_editor.pack(fill="both", expand=True)
    # # Bind the key release event inside text_editor to our reader function
    # # tk.Text() has no native function to read text in real time, this is the best option
    # text_editor.bind("<KeyRelease>", lambda event: on_key_release_latex_editor(event, text_editor))

    # # LaTeX Output Container
    # latex_output_container = tk.Frame(latex_frame, bg=COLORS["bg_input"], bd=1, highlightbackground=COLORS["border"], highlightthickness=1, height=150)
    # latex_output_container.pack(fill=tk.X, pady=(5, 20))
    # # Fix the height of the LaTeX Output Container
    # latex_output_container.pack_propagate(False)

    # # LaTeX Image Output (incomplete)
    # preview_label = tk.Frame(latex_output_container, bg="white")
    # preview_label.pack(fill="both", expand=True)

    # # Initialise the latex window the moment the output frame is mounted
    # global canvas
    # canvas = latex.init_latex_window_codecogs(preview_label, "white")

    # # LaTeX compiler button and key listener
    # compile_button = tk.Button(editor_container, text="Compile", bg=COLORS["border"], fg=COLORS["text_main"], bd=0, relief="flat", font=FONTS["font_subtitle"], command=(lambda: compile_latex_codecogs(canvas)))
    # compile_button.pack(side="right")

    # # Listen to Enter key anywhere
    # root.bind("<Return>", lambda event: compile_latex_codecogs(canvas))
    # text_editor.bind("<Return>", lambda event: compile_latex_codecogs(canvas))

    # # Listen for Shift + Enter for breaklines
    # root.bind("<Shift-Return>", lambda event: None)
    # text_editor.bind("<Shift-Return>", lambda event: None)

    # # Clicking anywhere outside the text editor frame makes us lose active focus
    # root.bind("<Button-1>", lambda event: event.widget.focus_set())