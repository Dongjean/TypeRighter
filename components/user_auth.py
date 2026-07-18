import tkinter as tk
from tkinter import font as tkfont
# from urllib.error import HTTPError
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException
import json

import main as main
import utils.firebase_app as fb
import utils.auth as auth
import utils.settings as settings
import utils.templates as templates
import utils.shortcuts_unicode as shortcuts_unicode

user_info = {
    "email": None
}

def login(root, username_editor, password_editor, login_error_label, login_hub_container, auth_frame, COLORS, FONTS):
    username = username_editor.get()
    password = password_editor.get()

    # Login on firebase
    try:
        user = fb.auth.sign_in_with_email_and_password(username, password)
        print(user)
        refresh_token = user["refreshToken"]
        id_token = user["idToken"]
        user_email = user["email"]

        user_info["email"] = user_email

        status, e = auth.login(id_token, refresh_token, user_email, None)
        if status:
            # If Login is successful
            login_error_label.configure(text=f"Successfully Logged In As: {user_email}", fg=COLORS["action_green"])
            
            # Clear the username and password entries
            username_editor.delete(0, "end")
            password_editor.delete(0, "end")
            
            # Load the settings
            curr_settings = settings.load(username)

            # Load the current template
            templates.load(username)
            templates.use_template(curr_settings["curr_template"])
            shortcuts_unicode.load()

            main.update_breakout_key()

            # Destroy the login frame
            destroy_login_frame(root, login_hub_container)

            # Build the user_info frame
            build_user_info_frame(root, auth_frame, COLORS, FONTS)

        else:
            # If Login is not successful
            print(e)
            login_error_label.configure(text="Please Try Again")

    except HTTPError as e:
        json_error = json.loads(e.strerror)["error"]
        error_code = json_error["code"]
        error_message = json_error["message"]

        print(error_code)
        print(error_message)

        # For Regular Login Problems
        if error_code == 400:
            
            # Wrong Email
            if error_message == "INVALID_EMAIL":
                login_error_label.configure(text="Incorrect Email")

            # Correct Email, Wrong Password
            elif error_message == "INVALID_LOGIN_CREDENTIALS":
                login_error_label.configure(text="Incorrect Password")
        
        # Catch any stray errors
        else:
            login_error_label.configure(text="Please Try Again")
            print("There was an Issue Logging in")

    except ConnectionError as e:
        login_error_label.configure(text="Please Check Your Connection")
        print(f"error while logging into Firebase: {e}")
    except Timeout as e:
        login_error_label.configure(text="Timeout, Please Try Again")
        print(f"error while logging into Firebase: {e}")
    except RequestException as e:
        login_error_label.configure(text="Please Try Again")
        print(f"error while logging into Firebase: {e}")
    except Exception as e:
        login_error_label.configure(text="Please Try Again")
        print(f"error while logging into Firebase: {e}")

def signup(username_editor, password_editor, signup_error_label, COLORS):
    username = username_editor.get()
    password = password_editor.get()

    # Signup on firebase
    try:
        fb.auth.create_user_with_email_and_password(username, password)

        # If Signup is successful
        signup_error_label.configure(text="Successfully Created Account, You May Login Now", fg=COLORS["action_green"])
        
        # Clear the username and password entries
        username_editor.delete(0, "end")
        password_editor.delete(0, "end")

    except HTTPError as e:
        json_error = json.loads(e.strerror)["error"]
        error_code = json_error["code"]
        error_message = json_error["message"]

        print(error_code)
        print(error_message)

        # For Regular Signup Problems
        if error_code == 400:
            
            # Bad Email
            if error_message == "INVALID_EMAIL":
                signup_error_label.configure(text="Bad Email")
            
            elif error_message == "EMAIL_EXISTS":
                signup_error_label.configure(text="This Email Already Exists")

            # Good Email, but Weak Password
            elif error_message == "WEAK_PASSWORD : Password should be at least 6 characters":
                signup_error_label.configure(text="Password must be at least 6 characters")
        
        # Catch any stray errors
        else:
            signup_error_label.configure(text="Please Try Again")
            print(f"error while signing up for Firebase: {e}")

    except ConnectionError as e:
        signup_error_label.configure(text="Please Check Your Connection")
        print(f"error while signing up for Firebase: {e}")
    except Timeout as e:
        signup_error_label.configure(text="Timeout, Please Try Again")
        print(f"error while signing up for Firebase: {e}")
    except RequestException as e:
        signup_error_label.configure(text="Please Try Again")
        print(f"error while signing up for Firebase: {e}")
    except Exception as e:
        signup_error_label.configure(text="Please Try Again")
        print(f"error while signing up for Firebase: {e}")

def logout(root, user_info_container, auth_frame, COLORS, FONTS):
    global user_info

    # Delete the folder for this user's user data
    templates.delete_user_data(user_info["email"])

    user_info = {
        "email": None
    }

    auth.logout()

    # Maintain the current template, but change the current name to 'default'
    settings.set_setting("curr_template", "default")

    # Destroy the user_info frame
    destroy_user_info_frame(root, user_info_container)

    # Build the login frame
    build_login_frame(root, auth_frame, COLORS, FONTS)

def build_user_auth(root, COLORS, FONTS):
    
    # Frame for user login page
    auth_frame = tk.Frame(root, bg=COLORS["bg_main"], padx=20, pady=20, takefocus=True, name="auth_frame")
    auth_frame.pack(side="top", fill="both", expand=True)

    # Header Titles
    # Set to be at the top, centred (expand=False by default)
    title_label = tk.Label(auth_frame, text="Login", fg=COLORS["text_main"], bg=COLORS["bg_main"], font=FONTS["font_title"], name="title_label")
    title_label.pack(fill="x", pady=0)

    # Start with the login frame, iff we are NOT logged in already
    email, e = auth.get_email()
    if not email:
        build_login_frame(root, auth_frame, COLORS, FONTS)
    # If we are logged in, display the logged in user and logout button
    else:
        global user_info
        user_info["email"] = email
        build_user_info_frame(root, auth_frame, COLORS, FONTS)

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


# User info init and destroyer
def build_user_info_frame(root, auth_frame, COLORS, FONTS):

    email = user_info["email"]
    
    # User Info Container
    user_info_container = tk.Frame(auth_frame, bg=COLORS["bg_main"], bd=0, name="user_info_container")
    user_info_container.pack(expand=True)
    
    # Email Label
    email_label = tk.Label(user_info_container, text=f"Current Logged Email: {email}", bg=COLORS["bg_main"], fg=COLORS["text_main"], bd=0, font=FONTS["font_subtitle"], name="email_label")
    email_label.pack()

    # Logout Button
    logout_button = tk.Button(user_info_container, text="Logout", bg=COLORS["border"], fg=COLORS["text_main"], bd=0, relief="flat", font=FONTS["font_subtitle"], command=(lambda: logout(root, user_info_container, auth_frame, COLORS, FONTS)), name="logout_button")
    logout_button.pack(side="bottom")

def destroy_user_info_frame(root, user_info_container):

    # Destroy the user info container
    user_info_container.destroy()

# Login frame init and destroyer
def build_login_frame(root, auth_frame, COLORS, FONTS):
    
    # Login Hub Container
    login_hub_container = tk.Frame(auth_frame, bg=COLORS["bg_main"], bd=0, name="login_hub_container")
    login_hub_container.pack(expand=True)
    
    # Error Message
    login_error_label = tk.Label(login_hub_container, text="", bg=COLORS["bg_main"], fg=COLORS["error_red"], bd=0, font=FONTS["font_subtitle"], name="login_error_label")
    login_error_label.pack()

    # Username Frame
    username_frame = tk.Frame(login_hub_container, bg=COLORS["bg_main"], bd=0, name="username_frame")
    username_frame.pack(expand=True, pady=5)
    username_label = tk.Label(username_frame, text="Username: ", bg=COLORS["bg_main"], fg=COLORS["text_main"], bd=0, font=FONTS["font_subtitle"], name="username_label")
    username_label.pack(side="left")
    username_editor = tk.Entry(username_frame, bg=COLORS["bg_input"], fg=COLORS["text_main"], insertbackground="white", bd=1, highlightbackground=COLORS["border"], highlightthickness=1, font=FONTS["font_subtitle"], name="username_editor")
    username_editor.pack(side="right")
  
    # Password Frame
    password_frame = tk.Frame(login_hub_container, bg=COLORS["bg_main"], bd=0, name="password_frame")
    password_frame.pack(expand=True, pady=5)
    password_label = tk.Label(password_frame, text="Password: ", bg=COLORS["bg_main"], fg=COLORS["text_main"], bd=0, font=FONTS["font_subtitle"], name="password_label")
    password_label.pack(side="left")
    password_editor = tk.Entry(password_frame, bg=COLORS["bg_input"], fg=COLORS["text_main"], insertbackground="white", bd=1, highlightbackground=COLORS["border"], highlightthickness=1, font=FONTS["font_subtitle"], name="password_editor")
    password_editor.pack(side="right")

    # Login Button
    login_button = tk.Button(login_hub_container, text="Login", bg=COLORS["border"], fg=COLORS["text_main"], bd=0, relief="flat", font=FONTS["font_subtitle"], command=(lambda: login(root, username_editor, password_editor, login_error_label, login_hub_container, auth_frame, COLORS, FONTS)), name="login_button")
    login_button.pack(side="bottom")

    # Clicking anywhere outside the text editor frame makes us lose active focus
    root.bind("<Button-1>", lambda event: event.widget.focus_set())
    # Enter keybind to login
    root.bind("<Return>", lambda event: login(root, username_editor, password_editor, login_error_label, login_hub_container, auth_frame, COLORS, FONTS))

    # Change to Signup Button
    change_frame = tk.Frame(login_hub_container, bg=COLORS["bg_main"], bd=0, name="change_frame")
    change_frame.pack(side="bottom")
    change_text = tk.Label(change_frame, text="Don't have an account? ", bg=COLORS["bg_main"], fg=COLORS["text_main"], bd=0, font=FONTS["font_subtitle"], name="change_text")
    change_text.pack(side="left")
    change_button = tk.Label(change_frame, text="Signup Now", bg=COLORS["bg_main"], fg=COLORS["hyperlink_blue"], bd=0, font=FONTS["font_hyperlink"], cursor="hand2", name="change_button")
    change_button.pack(side="left")

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
    signup_hub_container = tk.Frame(auth_frame, bg=COLORS["bg_main"], bd=0, name="signup_hub_container")
    signup_hub_container.pack(expand=True)
    
    # Error Message
    signup_error_label = tk.Label(signup_hub_container, text="", bg=COLORS["bg_main"], fg=COLORS["error_red"], bd=0, font=FONTS["font_subtitle"], name="signup_error_label")
    signup_error_label.pack()

    # Username Frame
    username_frame = tk.Frame(signup_hub_container, bg=COLORS["bg_main"], bd=0, name="username_frame")
    username_frame.pack(expand=True, pady=5)
    username_label = tk.Label(username_frame, text="Username: ", bg=COLORS["bg_main"], fg=COLORS["text_main"], bd=0, font=FONTS["font_subtitle"], name="username_label")
    username_label.pack(side="left")
    username_editor = tk.Entry(username_frame, bg=COLORS["bg_input"], fg=COLORS["text_main"], insertbackground="white", bd=1, highlightbackground=COLORS["border"], highlightthickness=1, font=FONTS["font_subtitle"], name="username_editor")
    username_editor.pack(side="right")
  
    # Password Frame
    password_frame = tk.Frame(signup_hub_container, bg=COLORS["bg_main"], bd=0, name="password_frame")
    password_frame.pack(expand=True, pady=5)
    password_label = tk.Label(password_frame, text="Password: ", bg=COLORS["bg_main"], fg=COLORS["text_main"], bd=0, font=FONTS["font_subtitle"], name="password_label")
    password_label.pack(side="left")
    password_editor = tk.Entry(password_frame, bg=COLORS["bg_input"], fg=COLORS["text_main"], insertbackground="white", bd=1, highlightbackground=COLORS["border"], highlightthickness=1, font=FONTS["font_subtitle"], name="password_editor")
    password_editor.pack(side="right")

    # Signup Button
    signup_button = tk.Button(signup_hub_container, text="Signup", bg=COLORS["border"], fg=COLORS["text_main"], bd=0, relief="flat", font=FONTS["font_subtitle"], command=(lambda: signup(username_editor, password_editor, signup_error_label, COLORS)), name="signup_button")
    signup_button.pack(side="bottom")
    # Enter keybind to signup
    root.bind("<Return>", lambda event: signup(username_editor, password_editor, signup_error_label, COLORS))

    # Change to Login Button
    change_frame = tk.Frame(signup_hub_container, bg=COLORS["bg_main"], bd=0, name="change_frame")
    change_frame.pack(side="bottom")
    change_text = tk.Label(change_frame, text="Already have an account? ", bg=COLORS["bg_main"], fg=COLORS["text_main"], bd=0, font=FONTS["font_subtitle"], name="change_text")
    change_text.pack(side="left")
    change_button = tk.Label(change_frame, text="Login Now", bg=COLORS["bg_main"], fg=COLORS["hyperlink_blue"], bd=0, font=FONTS["font_hyperlink"], cursor="hand2", name="change_button")
    change_button.pack(side="left")
    
    # Click bind to change signup --> login
    if not user_info["email"]:
        change_button.bind("<Button-1>", lambda event: change_login_signup(root, auth_frame, COLORS, FONTS, signup_hub_container, "signup", "login"))
    
    # Click bidn to change signup --> user_info
    else:
        change_button.bind("<Button-1>", lambda event: change_login_signup(root, auth_frame, COLORS, FONTS, signup_hub_container, "signup", "user_info"))

def destroy_signup_frame(root, signup_hub_container):

    # Destroy the signup hub container
    signup_hub_container.destroy()

    # Unbind the login keybind
    root.unbind("<Return>")

    # Unbind the change to signup button bind
    root.unbind("<Button-1>")