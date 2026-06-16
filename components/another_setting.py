import tkinter as tk

def build_another_setting(settings_subwindow_container, COLORS, FONTS):

    # Preferences Frame
    another_frame = tk.Frame(settings_subwindow_container, bg=COLORS["bg_input"], takefocus=True, name="another_frame")
    another_frame.pack(fill="both")

    # Label
    placeholder_label = tk.Label(another_frame, bg=COLORS["bg_input"], font=FONTS["font_subtitle"], fg=COLORS["text_main"], text="another")
    placeholder_label.pack()

def destroy_another_setting(settings_subwindow_container):
    for widget in settings_subwindow_container.winfo_children():
        widget.destroy()