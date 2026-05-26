import tkinter as tk
from tkinter import font as tkfont

username = ""
password = ""

def login(username, password):
    print(f"loggin in for {username}, {password}")

# Text input reader for username input
def on_key_release_username_editor(event, text_editor):
    global username
    # Get all text minus the auto-added trailing newline
    username = text_editor.get()

# Text input reader for password input
def on_key_release_password_editor(event, text_editor):
    global password
    # Get all text minus the auto-added trailing newline
    password = text_editor.get()

def build_user_auth(root, COLORS, FONTS):

    # Reset root for a clean overlay init
    # Remove all child widgets except for the navbar
    for widget in root.winfo_children():
        if widget.winfo_name() != "navbar_frame":
          widget.destroy()
    
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
    username_frame = tk.Frame(login_hub_container, bg=COLORS["bg_input"], bd=1, highlightbackground=COLORS["border"], highlightthickness=1)
    username_frame.pack(fill="x", expand=True)
    username_label = tk.Label(username_frame, text="Username: ", bg=COLORS["bg_input"], fg=COLORS["text_main"], bd=0, font=FONTS["font_subtitle"])
    username_label.pack(side="left")
    username_editor = tk.Entry(username_frame, bg=COLORS["bg_input"], fg=COLORS["text_main"], insertbackground="white", bd=0, font=FONTS["font_subtitle"])
    username_editor.pack(side="right")
    # Bind the key release event inside text editor to our reader function
    # tk.Text() has no native function to read text in real time, this is the best option
    username_editor.bind("<KeyRelease>", lambda event: on_key_release_username_editor(event, username_editor))
  
    # Password Frame
    password_frame = tk.Frame(login_hub_container, bg=COLORS["bg_input"], bd=1, highlightbackground=COLORS["border"], highlightthickness=1)
    password_frame.pack(fill="x", expand=True)
    password_label = tk.Label(password_frame, text="Password: ", bg=COLORS["bg_input"], fg=COLORS["text_main"], bd=0, font=FONTS["font_subtitle"])
    password_label.pack(side="left")
    password_editor = tk.Entry(password_frame, bg=COLORS["bg_input"], fg=COLORS["text_main"], insertbackground="white", bd=0, font=FONTS["font_subtitle"])
    password_editor.pack(side="right")
    # Bind the key release event inside text editor to our reader function
    # tk.Text() has no native function to read text in real time, this is the best option
    password_editor.bind("<KeyRelease>", lambda event: on_key_release_password_editor(event, password_editor))

    # Login Button
    login_button = tk.Button(login_hub_container, text="Login", bg=COLORS["border"], fg=COLORS["text_main"], bd=0, relief="flat", font=FONTS["font_subtitle"], command=(lambda: login(username, password)))
    login_button.pack(side="bottom")

    # Clicking anywhere outside the text editor frame makes us lose active focus
    root.bind("<Button-1>", lambda event: event.widget.focus_set())