import tkinter as tk
from tkinter import font as tkfont

def login(username_editor, password_editor):
    username = username_editor.get()
    password = password_editor.get()
    print(f"loggin in for {username}, {password}")

def build_user_auth(root, COLORS, FONTS):
    
    # Frame for user login page
    auth_frame = tk.Frame(root, bg=COLORS["bg_main"], padx=20, pady=20, takefocus=True, name="auth_frame")
    auth_frame.pack(side="top", fill="both", expand=True)

    # Header Titles
    # Set to be at the top, centred (expand=False by default)
    title_label = tk.Label(auth_frame, text="Login", fg=COLORS["text_main"], bg=COLORS["bg_main"], font=FONTS["font_title"])
    title_label.pack(fill="x", pady=0)

    # Login Hub Container
    login_hub_container = tk.Frame(auth_frame, bg=COLORS["bg_main"], bd=0)
    login_hub_container.pack(expand=True)

    # Username Frame
    username_frame = tk.Frame(login_hub_container, bg=COLORS["bg_main"], bd=0)
    username_frame.pack(fill="x", expand=True, pady=5)
    username_label = tk.Label(username_frame, text="Username: ", bg=COLORS["bg_main"], fg=COLORS["text_main"], bd=0, font=FONTS["font_subtitle"])
    username_label.pack(side="left")
    username_editor = tk.Entry(username_frame, bg=COLORS["bg_input"], fg=COLORS["text_main"], insertbackground="white", bd=1, highlightbackground=COLORS["border"], highlightthickness=1, font=FONTS["font_subtitle"])
    username_editor.pack(side="right")
  
    # Password Frame
    password_frame = tk.Frame(login_hub_container, bg=COLORS["bg_main"], bd=0)
    password_frame.pack(fill="x", expand=True, pady=5)
    password_label = tk.Label(password_frame, text="Password: ", bg=COLORS["bg_main"], fg=COLORS["text_main"], bd=0, font=FONTS["font_subtitle"])
    password_label.pack(side="left")
    password_editor = tk.Entry(password_frame, bg=COLORS["bg_input"], fg=COLORS["text_main"], insertbackground="white", bd=1, highlightbackground=COLORS["border"], highlightthickness=1, font=FONTS["font_subtitle"])
    password_editor.pack(side="right")

    # Login Button
    login_button = tk.Button(login_hub_container, text="Login", bg=COLORS["border"], fg=COLORS["text_main"], bd=0, relief="flat", font=FONTS["font_subtitle"], command=(lambda: login(username_editor, password_editor)))
    login_button.pack(side="bottom")

    # Clicking anywhere outside the text editor frame makes us lose active focus
    root.bind("<Button-1>", lambda event: event.widget.focus_set())

# Destroy function to tear down user auth page
def destroy_user_auth(root):

    # Remove all child widgets except for the navbar
    for widget in root.winfo_children():
        if widget.winfo_name() != "navbar_frame":
          widget.destroy()

    # Nothing else for user auth