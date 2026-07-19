import tkinter as tk
from tkinter import ttk

from tkinter import font as tkfont

import views.view_handler as view_handler


import components.latex_workspace as latex_workspace
import components.user_auth as user_auth
import components.unicode_searchpanel as unicode_search
import components.settings_window as settings_window

import main as main
import utils.settings as settings
import utils.templates as templates
import utils.shortcuts_unicode as shortcuts_unicode
import utils.auth as auth

curr_window = ""
init_functions = {
    "latex-workspace": latex_workspace.build_latex_workspace,
    "user-auth": user_auth.build_user_auth,
    "unicode-search": unicode_search.build_unicode_search_panel,
    "settings-window": settings_window.build_settings_window,
}

destroy_functions = {
    "latex-workspace": latex_workspace.destroy_latex_workspace,
    "user-auth": user_auth.destroy_user_auth,
    "unicode-search": unicode_search.destroy_unicode_search_panel,
    "settings-window": settings_window.destroy_settings_windows,
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

def reload_window(selected_window, root, COLORS, FONTS):
    global curr_window

    # Do things iff the window is unchanged (for reloading windows)
    if selected_window == curr_window:
        
        # First, destroy the window
        if selected_window in destroy_functions:
            destroy_functions[selected_window](root=root)
        else:
            print(f"No function found to destroy {selected_window}")
        
        # Then, initialise the new window
        if selected_window in init_functions:
            init_functions[selected_window](root=root, COLORS=COLORS, FONTS=FONTS)
        else:
            print(f"No function found to initialise {selected_window}")

def on_template_selection(event, template_selector, root, COLORS, FONTS):
    
    # Get the current value from the combobox
    selected_template = template_selector.get()
    
    if selected_template:
        templates.use_template(selected_template)
        curr_user, e = auth.get_email()
        settings.set_setting("curr_template", selected_template, curr_user)
        shortcuts_unicode.load()
        main.update_breakout_key()
        reload_window(curr_window, root, COLORS, FONTS)

def build_navbar(root, COLORS, FONTS, WINDOWS, start_window):

    # Frame for navbar
    navbar_frame = tk.Frame(root, bg=COLORS["bg_main"], takefocus=True, name="navbar_frame")
    navbar_frame.pack(side="right", fill="both")

    # Display each window as a custom button
    navbar_frame.selected_window = tk.StringVar(value=start_window)
    for key, value in WINDOWS.items():
        btn = tk.Radiobutton(navbar_frame, text=value["name"], variable=navbar_frame.selected_window, value=key, bg=COLORS["border"], fg=COLORS["text_main"], bd=0, relief="flat", width=10, height=3, font=FONTS["font_subtitle"], selectcolor=COLORS["accent_blue"], activebackground=COLORS["accent_blue"], indicatoron=False, command=(lambda: change_window(navbar_frame.selected_window.get(), root, COLORS, FONTS)), name=key)
        btn.pack(side="top")
    
    email, e = auth.get_email()
    if email:
        # List of templates
        curr_templates = templates.all_templates(email)
        curr_template_names = list(curr_templates)
        
        # Template Selector Dropdown Menu
        template_selector = ttk.Combobox(navbar_frame, values=curr_template_names, state="readonly")
        curr_selected_template = settings.lookup_setting("curr_template")
        template_selector.set(curr_selected_template)
        template_selector.pack()
        template_selector.bind("<<ComboboxSelected>>", lambda event: on_template_selection(event, template_selector, root, COLORS, FONTS))

    # Manually initialise the first window
    # Clear curr_window first jic we exited control panel view and re-entere
    global curr_window
    curr_window = ""
    change_window(start_window, root, COLORS, FONTS)