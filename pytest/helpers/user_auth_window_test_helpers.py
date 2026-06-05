from helpers.main_test_helpers import check_tk_exists, check_widget_props

def get_user_auth_build_tests(root, FONTS, COLORS):

    # Check if all the widgets exist
    auth_frame, is_auth_frame = check_tk_exists(root, "auth_frame")
    title_label, is_title_label = check_tk_exists(auth_frame, "title_label")
    login_hub_container, is_login_hub_container = check_tk_exists(auth_frame, "login_hub_container")
    username_frame, is_username_frame = check_tk_exists(login_hub_container, "username_frame")
    username_label, is_username_label = check_tk_exists(username_frame, "username_label")
    username_editor, is_username_editor = check_tk_exists(username_frame, "username_editor")
    password_frame, is_password_frame = check_tk_exists(login_hub_container, "password_frame")
    password_label, is_password_label = check_tk_exists(password_frame, "password_label")
    password_editor, is_password_editor = check_tk_exists(password_frame, "password_editor")
    login_button, is_login_button = check_tk_exists(login_hub_container, "login_button")
    change_frame, is_change_frame = check_tk_exists(login_hub_container, "change_frame")
    change_text, is_change_text = check_tk_exists(change_frame, "change_text")
    change_button, is_change_button = check_tk_exists(change_frame, "change_button")

    # Check the properties of each widget

    # auth_frame
    auth_frame_props = [
        ("config", "bg", COLORS["bg_main"]),
        ("config", "padx", 20),
        ("config", "pady", 20),
        ("config", "takefocus", "1"),

        ("pack", "side", "top"),
        ("pack", "fill", "both"),
        ("pack", "expand", True),

        ("misc", "widget_name", "auth_frame")
    ]
    is_auth_frame_props = check_widget_props(auth_frame, auth_frame_props)

    # title_label
    title_label_props = [
        ("config", "text", "Login"),
        ("config", "bg", COLORS["bg_main"]),
        ("config", "fg", COLORS["text_main"]),

        ("pack", "fill", "x"),
        ("pack", "pady", 0),

        ("misc", "widget_name", "title_label"),

        ("misc", "font", FONTS["font_title"].actual())
    ]
    is_title_label_props = check_widget_props(title_label, title_label_props)


    # login_hub_container
    login_hub_container_props = [
        ("config", "bg", COLORS["bg_input"]),
        ("config", "bd", 0),

        ("pack", "expand", True),

        ("misc", "widget_name", "login_hub_container"),
    ]
    is_login_hub_container_props = check_widget_props(login_hub_container, login_hub_container_props)

    # username_frame
    username_frame_props = [
        ("config", "bg", COLORS["bg_main"]),
        ("config", "bd", 0),

        ("pack", "expand", True),
        ("pack", "pady", 5),

        ("misc", "widget_name", "username_frame"),
    ]
    is_username_frame_props = check_widget_props(username_frame, username_frame_props)

    # username_label
    username_label_props = [
        ("config", "text", "Username: "),
        ("config", "bg", COLORS["bg_main"]),
        ("config", "fg", COLORS["text_main"]),
        ("config", "bd", 0),

        ("pack", "side", "left"),

        ("misc", "widget_name", "username_label"),

        ("misc", "font", FONTS["font_subtitle"].actual())
    ]
    is_username_label_props = check_widget_props(username_label, username_label_props)

    # username_editor
    username_editor_props = [
        ("config", "bg", COLORS["bg_input"]),
        ("config", "fg", COLORS["text_main"]),
        ("config", "insertbackground", "white"),
        ("config", "bd", 1),
        ("config", "highlightbackground", 1),

        ("pack", "side", "right"),

        ("misc", "widget_name", "username_editor"),

        ("misc", "font", FONTS["font_subtitle"].actual())
    ]
    is_username_editor_props = check_widget_props(username_editor, username_editor_props)

    # password_frame
    password_frame_props = [
        ("config", "bg", COLORS["bg_main"]),
        ("config", "bd", 0),

        ("pack", "expand", True),
        ("pack", "pady", 5),

        ("misc", "widget_name", "password_frame"),
    ]
    is_password_frame_props = check_widget_props(password_frame, password_frame_props)

    # password_label
    password_label_props = [
        ("config", "text", "Username: "),
        ("config", "bg", COLORS["bg_main"]),
        ("config", "fg", COLORS["text_main"]),
        ("config", "bd", 0),

        ("pack", "side", "left"),

        ("misc", "widget_name", "password_label"),

        ("misc", "font", FONTS["font_subtitle"].actual())
    ]
    is_password_label_props = check_widget_props(password_label, password_label_props)

    # password_editor
    password_editor_props = [
        ("config", "bg", COLORS["bg_input"]),
        ("config", "fg", COLORS["text_main"]),
        ("config", "insertbackground", "white"),
        ("config", "bd", 1),
        ("config", "highlightbackground", 1),

        ("pack", "side", "right"),

        ("misc", "widget_name", "password_editor"),

        ("misc", "font", FONTS["font_subtitle"].actual())
    ]
    is_password_editor_props = check_widget_props(password_editor, password_editor_props)

    # login_button
    login_button_props = [
        ("config", "text", "Login"),
        ("config", "bg", COLORS["border"]),
        ("config", "fg", COLORS["text_main"]),
        ("config", "bd", 0),
        ("config", "relief", "flat"),
        ("config", "command", True), # Check that a function is linked to command

        ("pack", "side", "bottom"),

        ("misc", "widget_name", "login_button"),

        ("misc", "font", FONTS["font_subtitle"].actual())
    ]
    is_login_button_props = check_widget_props(login_button, login_button_props)

    # change_frame
    change_frame_props = [
        ("config", "bg", COLORS["bg_main"]),
        ("config", "bd", 0),

        ("pack", "side", "bottom"),

        ("misc", "widget_name", "change_frame"),
    ]
    is_change_frame_props = check_widget_props(change_frame, change_frame_props)

    # change_text
    change_text_props = [
        ("config", "text", "Don't have an account? "),
        ("config", "bg", COLORS["bg_main"]),
        ("config", "fg", COLORS["text_main"]),
        ("config", "bd", 0),

        ("pack", "side", "left"),

        ("misc", "widget_name", "change_text"),

        ("misc", "font", FONTS["font_subtitle"].actual())
    ]
    is_change_text_props = check_widget_props(change_text, change_text_props)

    # change_button
    change_button_props = [
        ("config", "text", "Login"),
        ("config", "bg", COLORS["bg_main"]),
        ("config", "fg", COLORS["hyperlink_blue"]),
        ("config", "bd", 0),
        ("config", "relief", "flat"),
        ("config", "cursor", "hand2"),

        ("pack", "side", "left"),

        ("misc", "widget_name", "change_button"),

        ("misc", "font", FONTS["font_hyperlink"].actual()),

        ("misc", "bind", "<Button-1>")
    ]
    is_change_button_props = check_widget_props(change_button, change_button_props)

    # root
    root_props = [
        ("misc", "bind", "<Key-Return>")
    ]
    is_root_props = check_widget_props(root, root_props)

    return {
        "is_auth_frame": is_auth_frame,
        "is_title_label": is_title_label,
        "is_login_hub_container": is_login_hub_container,
        "is_username_frame": is_username_frame,
        "is_username_label": is_username_label,
        "is_username_editor": is_username_editor,
        "is_password_frame": is_password_frame,
        "is_password_label": is_password_label,
        "is_password_editor": is_password_editor,
        "is_login_button": is_login_button,
        "is_change_frame": is_change_frame,
        "is_change_text": is_change_text,
        "is_change_button": is_change_button,
        "is_auth_frame_props": is_auth_frame_props,
        "is_title_label_props": is_title_label_props,
        "is_login_hub_container_props": is_login_hub_container_props,
        "is_username_frame_props": is_username_frame_props,
        "is_username_label_props": is_username_label_props,
        "is_username_editor_props": is_username_editor_props,
        "is_password_frame_props": is_password_frame_props,
        "is_password_label_props": is_password_label_props,
        "is_password_editor_props": is_password_editor_props,
        "is_login_button_props": is_login_button_props,
        "is_change_frame_props": is_change_frame_props,
        "is_change_text_props": is_change_text_props,
        "is_change_button_props": is_change_button_props,
        "is_root_props": is_root_props
    }