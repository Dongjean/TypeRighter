from helper_functions.main_test_helpers import check_tk_exists, check_widget_props
import utils.shortcuts_unicode as shortcuts_unicode

def get_settings_window_build_test(root, FONTS, COLORS):

    # Check if all the widgets exist
    settings_frame, is_settings_frame = check_tk_exists(root, "settings_frame")
    title_label, is_title_label = check_tk_exists(settings_frame, "title_label")
    subwindow_header, is_subwindow_header = check_tk_exists(settings_frame, "subwindow_header")
    subwindow_label, is_subwindow_label = check_tk_exists(subwindow_header, "subwindow_label")
    back_button, is_back_button = check_tk_exists(subwindow_header, "back_button")
    settings_container, is_settings_container = check_tk_exists(settings_frame, "settings_container")
    settings_subwindow_container, is_settings_subwindow_container = check_tk_exists(settings_frame, "settings_subwindow_container")
    settings_selection_container, is_settings_selection_container = check_tk_exists(settings_frame, "settings_selection_container")

    # Check the properties of each widget

    # settings_frame
    settings_frame_props = [
        ("config", "bg", COLORS["bg_main"]),
        ("config", "padx", 20),
        ("config", "pady", 20),
        ("config", "takefocus", "1"),

        ("pack", "side", "top"),
        ("pack", "fill", "both"),
        ("pack", "expand", True),

        ("misc", "widget_name", "settings_frame")
    ]
    is_settings_frame_props = check_widget_props(settings_frame, settings_frame_props)

    # title_label
    title_label_props = [
        ("config", "text", "Settings"),
        ("config", "bg", COLORS["bg_main"]),
        ("config", "fg", COLORS["text_main"]),

        ("pack", "fill", "x"),
        ("pack", "pady", 0),

        ("misc", "widget_name", "title_label"),

        ("misc", "font", FONTS["font_title"].actual())
    ]
    is_title_label_props = check_widget_props(title_label, title_label_props)

    # subwindow_header
    subwindow_header_props = [
        ("config", "bg", COLORS["bg_main"]),

        ("pack", "fill", "x"),
        ("pack", "pady", 0),

        ("misc", "widget_name", "subwindow_header"),
    ]
    is_subwindow_header_props = check_widget_props(subwindow_header, subwindow_header_props)

    # subwindow_label
    subwindow_label_props = [
        ("config", "text", "All Settings"),
        ("config", "fg", COLORS["text_muted"]),
        ("config", "bg", COLORS["bg_main"]),
        ("config", "bd", 0),

        ("pack", "fill", "none"),
        ("pack", "anchor", "center"),
        ("pack", "side", "right"),
        ("pack", "expand", True),
        ("pack", "pady", 0),

        ("misc", "widget_name", "subwindow_label"),
        
        ("misc", "font", FONTS["font_subtitle"].actual())
    ]
    is_subwindow_label_props = check_widget_props(subwindow_label, subwindow_label_props)
    
    # back_button
    back_button_props = [
        ("config", "text", "Back"),
        ("config", "bg", COLORS["border"]),
        ("config", "fg", COLORS["text_main"]),
        ("config", "bd", 0),
        ("config", "relief", "flat"),
        ("config", "activebackground", COLORS["accent_blue"]),
        ("config", "command", True), # Check that a function is linked to command

        ("pack", "fill", "none"),
        ("pack", "anchor", "w"),
        ("pack", "side", "left"),
        ("pack", "pady", 0),

        ("misc", "widget_name", "back_button"),
        
        ("misc", "font", FONTS["font_subtitle"].actual())
    ]
    is_back_button_props = check_widget_props(back_button, back_button_props)
    
    # settings_container
    settings_container_props = [
        ("config", "bg", COLORS["bg_input"]),
        ("config", "bd", 1),
        ("config", "highlightbackground", COLORS["border"]),
        ("config", "highlightthickness", 1),

        ("pack", "fill", "both"),
        ("pack", "expand", True),

        ("misc", "widget_name", "settings_container"),
    ]
    is_settings_container_props = check_widget_props(settings_container, settings_container_props)

    # Each settings selector button
    is_setting_selector_buttons = True
    is_setting_selector_buttons_props = True
    SETTINGS = {
        "preferences-setting": {
            "name": "Preferences"
        },
        "another-setting": {
            "name": "Another one!"
        },
    }
    for key, value in SETTINGS.items():
        curr_setting_selector_button, is_curr_setting_selector_button = check_tk_exists(settings_selection_container, key)

        # If even a single setting selector button isnt there, fail the check
        if not is_curr_setting_selector_button:
            is_setting_selector_buttons = False
            break
        else:
            curr_setting_selector_button_props = [
                ("config", "text", value["name"]),
                ("config", "bg", COLORS["border"]),
                ("config", "fg", COLORS["text_main"]),
                ("config", "bd", 0),
                ("config", "relief", "flat"),
                ("config", "height", 3),
                ("config", "activebackground", COLORS["accent_blue"]),
                ("config", "command", True), # Check that a function is linked to command
        
                ("pack", "side", "top"),
                ("pack", "fill", "x"),
        
                ("misc", "widget_name", key),
        
                ("misc", "font", FONTS["font_subtitle"].actual()),
            ]
            is_curr_setting_selector_button_props = check_widget_props(curr_setting_selector_button, curr_setting_selector_button_props)

            # If even a single setting selector button isnt there, fail the check
            if not is_curr_setting_selector_button_props:
                is_setting_selector_buttons_props = False
                break

    return {
        "is_settings_frame": is_settings_frame,
        "is_title_label": is_title_label,
        "is_subwindow_header": is_subwindow_header,
        "is_subwindow_label": is_subwindow_label,
        "is_back_button": is_back_button,
        "is_settings_container": is_settings_container,
        "is_settings_subwindow_container": is_settings_subwindow_container,
        "is_settings_selection_container": is_settings_selection_container,
        "is_settings_frame_props": is_settings_frame_props,
        "is_title_label_props": is_title_label_props,
        "is_subwindow_header_props": is_subwindow_header_props,
        "is_subwindow_label_props": is_subwindow_label_props,
        "is_back_button_props": is_back_button_props,
        "is_settings_container_props": is_settings_container_props,
        "is_setting_selector_buttons": is_setting_selector_buttons,
        "is_setting_selector_buttons_props": is_setting_selector_buttons_props,
    }
