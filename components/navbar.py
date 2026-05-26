import tkinter as tk

from tkinter import font as tkfont

import views.root_view as root_view


import components.latex_workspace as latex_workspace
import components.user_auth as user_auth

curr_window = ""
init_functions = {
    "latex-workspace": latex_workspace.build_latex_workspace,
    "user-auth": user_auth.build_user_auth,
}

def change_window(selected_window, root, COLORS, FONTS):
    global curr_window
    if selected_window != curr_window:
        print(selected_window)
        curr_window = selected_window
        if selected_window in init_functions:
            init_functions[selected_window](root=root, COLORS=COLORS, FONTS=FONTS)
        else:
            print(f"No function found to initialise {selected_window}")
destroy_functions = {
    "latex-workspace": latex_workspace.destroy_latex_workspace,
    "user-auth": user_auth.destroy_user_auth,
}

def change_window(selected_window, root, COLORS, FONTS):
    global curr_window

    # Do things iff the window was CHANGED
    if selected_window != curr_window:
        prev_window = curr_window
        curr_window = selected_window
        
        # First, destroy the previous window
        if prev_window in destroy_functions:
            destroy_functions[prev_window](root=root)
        else:
            print(f"No function found to destroy {prev_window}")
        
        # Then, initialise the new window
        if curr_window in init_functions:
            init_functions[curr_window](root=root, COLORS=COLORS, FONTS=FONTS)
        else:
            print(f"No function found to initialise {curr_window}")

def build_navbar(root, COLORS, FONTS, WINDOWS, start_window):

    # Frame for navbar
    navbar_frame = tk.Frame(root, bg=COLORS["bg_main"], takefocus=True, name="navbar_frame")
    navbar_frame.pack(side="right", fill="both")

    # Display each window as a custom button
    navbar_frame.selected_window = tk.StringVar(value=start_window)
    for key, value in WINDOWS.items():
        btn = tk.Radiobutton(navbar_frame, text=value["name"], variable=navbar_frame.selected_window, value=key, bg=COLORS["border"], fg=COLORS["text_main"], bd=0, relief="flat", width=10, height=3, font=FONTS["font_subtitle"], selectcolor=COLORS["accent_blue"], activebackground=COLORS["accent_blue"], indicatoron=False, command=(lambda: change_window(navbar_frame.selected_window.get(), root, COLORS, FONTS)))
        btn.pack(side="top")

    # Manually initialise the first window
    # Clear curr_window first jic we exited control panel view and re-entere
    global curr_window
    curr_window = ""
    change_window(start_window, root, COLORS, FONTS)