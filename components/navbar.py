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
    global curr_window
    curr_window = start_window
    for key, value in WINDOWS.items():
        btn = tk.Radiobutton(navbar_frame, text=value["name"], variable=navbar_frame.selected_window, value=key, bg=COLORS["border"], fg=COLORS["text_main"], bd=0, relief="flat", width=10, height=3, font=FONTS["font_subtitle"], selectcolor=COLORS["accent_blue"], activebackground=COLORS["accent_blue"], indicatoron=False, command=(lambda: change_window(navbar_frame.selected_window.get())))
        btn.pack(side="top")