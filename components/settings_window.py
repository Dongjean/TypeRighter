import tkinter as tk

from components.preferences_setting import build_preferences_setting, destroy_preferences_setting
from components.another_setting import build_another_setting, destroy_another_setting
import utils.scroll as scroll

is_selecting = True
curr_subwindow = ""

SETTINGS = {
    "preferences-setting": {
        "name": "Preferences"
    },
    "another-setting": {
        "name": "Another one!"
    },
}

destroy_functions = {
    "preferences-setting": destroy_preferences_setting,
    "another-setting": destroy_another_setting,
}

init_functions = {
    "preferences-setting": build_preferences_setting,
    "another-setting": build_another_setting,
}

def select_setting(selected_setting, settings_container, subwindow_label, COLORS, FONTS):
    global curr_subwindow
    settings_subwindow_container = settings_container.nametowidget("settings_subwindow_container")
    settings_selection_container = settings_container.nametowidget("settings_selection_container")

    curr_subwindow = selected_setting
    
    # Then, initialise the new window
    if curr_subwindow in init_functions:
        init_functions[curr_subwindow](settings_subwindow_container=settings_subwindow_container, COLORS=COLORS, FONTS=FONTS)
    else:
        print(f"No function found to initialise {curr_subwindow}")

    settings_subwindow_container.pack(fill="both", expand=True)
    settings_selection_container.pack_forget()

    # Update the subwindow label
    new_label = ""
    if curr_subwindow in SETTINGS:
        new_label = SETTINGS[curr_subwindow]["name"]
    subwindow_label.config(text=new_label)

def back(settings_frame, subwindow_label):
    global curr_subwindow
    settings_container = settings_frame.scrollable_frame.nametowidget("settings_container")
    settings_subwindow_container = settings_container.nametowidget("settings_subwindow_container")
    settings_selection_container = settings_container.nametowidget("settings_selection_container")

    # Destroy the setting subwindow
    if curr_subwindow in destroy_functions:
        destroy_functions[curr_subwindow](settings_subwindow_container)
    curr_subwindow = ""

    settings_subwindow_container.pack_forget()
    settings_selection_container.pack(fill="both", expand=True)

    # Update the subwindow label
    subwindow_label.config(text="All Settings")

def build_settings_window(root, COLORS, FONTS):

    # Frame for Settings Window
    settings_frame = tk.Frame(root, bg=COLORS["bg_main"], padx=20, pady=20, takefocus=True, name="settings_frame")
    settings_frame.pack(side="top", fill="both", expand=True)
    
    settings_frame = scroll.ScrollableFrame(root, bg=COLORS["bg_main"], padx=20, pady=20, takefocus=True, name="settings_frame")
    settings_frame.pack(side="top", fill="both", expand=True)

    # Header Titles
    # Set to be at the top, centred (expand=False by default)
    title_label = tk.Label(settings_frame.scrollable_frame, text="Settings", fg=COLORS["text_main"], bg=COLORS["bg_main"], font=FONTS["font_title"], name="title_label")
    title_label.pack(fill="x", pady=0)

    # Subwindow Header
    subwindow_header = tk.Frame(settings_frame.scrollable_frame, bg=COLORS["bg_main"], name="subwindow_header")
    subwindow_header.pack(fill="x", pady=0)

    # Subwindow Label
    subwindow_label = tk.Label(subwindow_header, text="All Settings", fg=COLORS["text_muted"], bg=COLORS["bg_main"], font=FONTS["font_subtitle"], name="subwindow_label")
    subwindow_label.pack(fill="none", anchor="center", side="right", expand=True, pady=0)

    # Back Button
    back_button = tk.Button(subwindow_header, text="Back", bg=COLORS["border"], fg=COLORS["text_main"], bd=0, relief="flat", font=FONTS["font_subtitle"], activebackground=COLORS["accent_blue"], command=(lambda: back(settings_frame, subwindow_label)), name="back_button")
    back_button.pack(fill="none", anchor="w", side="left", pady=0)

    # Settings Container to contain the settings selector and settings sub-windows
    # If is_selecting == True, we display the settings selection menu
    # If is_selecting == False, we display the individual settings sub-window
    settings_container = tk.Frame(settings_frame.scrollable_frame, bg=COLORS["bg_input"], bd=1, highlightbackground=COLORS["border"], highlightthickness=1, name="settings_container")
    settings_container.pack(fill="both", expand=True)
    
    # For is_selecting == False
    settings_subwindow_container = tk.Frame(settings_container, bg=COLORS["bg_input"], name="settings_subwindow_container")
    settings_subwindow_container.pack(fill="both", expand=True)

    # For is_selecting == True
    settings_selection_container = tk.Frame(settings_container, bg=COLORS["bg_input"], name="settings_selection_container")
    settings_selection_container.pack(fill="both", expand=True)

    # Display each window as a custom button
    for key, value in SETTINGS.items():
        btn = tk.Button(settings_selection_container, text=value["name"], bg=COLORS["border"], fg=COLORS["text_main"], bd=0, relief="flat", height=3, font=FONTS["font_subtitle"], activebackground=COLORS["accent_blue"], command=(lambda subwindow=key: select_setting(subwindow, settings_container, subwindow_label, COLORS, FONTS)), name=key)
        btn.pack(side="top", fill="x")
    
    if is_selecting:
        settings_subwindow_container.pack_forget()
    elif not is_selecting:
        settings_selection_container.pack_forget()

# Destroy function to tear down settings window
def destroy_settings_windows(root):

    # Remove all child widgets except for the navbar
    for widget in root.winfo_children():
        if widget.winfo_name() != "navbar_frame":
          widget.destroy()