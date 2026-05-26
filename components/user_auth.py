import tkinter as tk
from tkinter import font as tkfont

import utils.firebase_app as fb

def login(username_editor, password_editor):
    username = username_editor.get()
    password = password_editor.get()

    # Login on firebase
    try:
        fb.auth.sign_in_with_email_and_password(username, password)
    except Exception as e:
        print(e)

def signup(username_editor, password_editor):
    username = username_editor.get()
    password = password_editor.get()

    # Signup on firebase
    try:
        fb.auth.create_user_with_email_and_password(username, password)
    except Exception as e:
        print(e)

def build_user_auth(root, COLORS, FONTS):
    
    # Frame for user login page
    auth_frame = tk.Frame(root, bg=COLORS["bg_main"], padx=20, pady=20, takefocus=True, name="auth_frame")
    auth_frame.pack(side="top", fill="both", expand=True)

    # Header Titles
    # Set to be at the top, centred (expand=False by default)
    title_label = tk.Label(auth_frame, text="Login", fg=COLORS["text_main"], bg=COLORS["bg_main"], font=FONTS["font_title"])
    title_label.pack(fill="x", pady=0)

    # Start with the login frame
    build_login_frame(root, auth_frame, COLORS, FONTS)

# Destroy function to tear down user auth page
def destroy_user_auth(root):

    # Remove all child widgets except for the navbar
    for widget in root.winfo_children():
        if widget.winfo_name() != "navbar_frame":
          widget.destroy()

    # Unbind the enter keybind
    root.unbind("<Return>")

# Callback from <Button-1> to change the window's state from login mode to signup mode
def change_login_signup(root, auth_frame, COLORS, FONTS, to_destroy, FROM, TO):
    if FROM == "login" and TO == "signup":
        
        # Destroy the login frame
        destroy_login_frame(root, to_destroy)

        # Build the signup frame
        build_signup_frame(root, auth_frame, COLORS, FONTS)
    elif FROM == "signup" and TO == "login":

        # Destroy the signup frame
        destroy_signup_frame(root, to_destroy)

        # Build the login frame
        build_login_frame(root, auth_frame, COLORS, FONTS)

    return "break"

# Login frame init and destroyer
def build_login_frame(root, auth_frame, COLORS, FONTS):
    
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
    # Enter keybind to login
    root.bind("<Return>", lambda event: login(username_editor, password_editor))

    # Change to Signup Button
    change_text = tk.Label(login_hub_container, text="Don't have an account? ", bg=COLORS["border"], fg=COLORS["text_main"], bd=0, font=FONTS["font_subtitle"])
    change_text.pack(side="bottom")
    change_button = tk.Label(login_hub_container, text="Signup Now", bg=COLORS["border"], fg=COLORS["text_main"], bd=0, font=FONTS["font_subtitle"])
    change_button.pack(side="bottom")
    # Click bind to change login --> signup
    change_button.bind("<Button-1>", lambda event: change_login_signup(root, auth_frame, COLORS, FONTS, login_hub_container, "login", "signup"))

def destroy_login_frame(root, login_hub_container):

    # Destroy the login hub container
    login_hub_container.destroy()

    # Unbind the login keybind
    root.unbind("<Return>")

    # Unbind the change to signup button bind
    root.unbind("<Button-1>")

# Signup frame init and destroyer
def build_signup_frame(root, auth_frame, COLORS, FONTS):

    # Signup Hub Container
    signup_hub_container = tk.Frame(auth_frame, bg=COLORS["bg_main"], bd=0)
    signup_hub_container.pack(expand=True)

    # Username Frame
    username_frame = tk.Frame(signup_hub_container, bg=COLORS["bg_main"], bd=0)
    username_frame.pack(fill="x", expand=True, pady=5)
    username_label = tk.Label(username_frame, text="Username: ", bg=COLORS["bg_main"], fg=COLORS["text_main"], bd=0, font=FONTS["font_subtitle"])
    username_label.pack(side="left")
    username_editor = tk.Entry(username_frame, bg=COLORS["bg_input"], fg=COLORS["text_main"], insertbackground="white", bd=1, highlightbackground=COLORS["border"], highlightthickness=1, font=FONTS["font_subtitle"])
    username_editor.pack(side="right")
  
    # Password Frame
    password_frame = tk.Frame(signup_hub_container, bg=COLORS["bg_main"], bd=0)
    password_frame.pack(fill="x", expand=True, pady=5)
    password_label = tk.Label(password_frame, text="Password: ", bg=COLORS["bg_main"], fg=COLORS["text_main"], bd=0, font=FONTS["font_subtitle"])
    password_label.pack(side="left")
    password_editor = tk.Entry(password_frame, bg=COLORS["bg_input"], fg=COLORS["text_main"], insertbackground="white", bd=1, highlightbackground=COLORS["border"], highlightthickness=1, font=FONTS["font_subtitle"])
    password_editor.pack(side="right")

    # Signup Button
    signup_button = tk.Button(signup_hub_container, text="Signup", bg=COLORS["border"], fg=COLORS["text_main"], bd=0, relief="flat", font=FONTS["font_subtitle"], command=(lambda: signup(username_editor, password_editor)))
    signup_button.pack(side="bottom")
    # Enter keybind to signup
    root.bind("<Return>", lambda event: signup(username_editor, password_editor))

    # Change to Login Button
    change_text = tk.Label(signup_hub_container, text="Already have an account? ", bg=COLORS["border"], fg=COLORS["text_main"], bd=0, font=FONTS["font_subtitle"])
    change_text.pack(side="bottom")
    change_button = tk.Label(signup_hub_container, text="Login Now", bg=COLORS["border"], fg=COLORS["text_main"], bd=0, font=FONTS["font_subtitle"])
    change_button.pack(side="bottom")
    # Click bind to change signup --> login
    change_button.bind("<Button-1>", lambda event: change_login_signup(root, auth_frame, COLORS, FONTS, signup_hub_container, "signup", "login"))

def destroy_signup_frame(root, signup_hub_container):

    # Destroy the signup hub container
    signup_hub_container.destroy()

    # Unbind the login keybind
    root.unbind("<Return>")

    # Unbind the change to signup button bind
    root.unbind("<Button-1>")
