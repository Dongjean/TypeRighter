import tkinter as tk

def build_preferences_setting(settings_subwindow_container, COLORS, FONTS):

    # Preferences Frame
    preferences_frame = tk.Frame(settings_subwindow_container, bg=COLORS["bg_input"], takefocus=True, name="preferences_frame")
    preferences_frame.pack(fill="both")

    # Label
    placeholder_label = tk.Label(preferences_frame, bg=COLORS["bg_input"], font=FONTS["font_subtitle"], fg=COLORS["text_main"], text="preferences")
    placeholder_label.pack()

def destroy_preferences_setting(settings_subwindow_container):
    for widget in settings_subwindow_container.winfo_children():
        widget.destroy()