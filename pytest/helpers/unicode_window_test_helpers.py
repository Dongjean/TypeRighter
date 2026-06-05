import tkinter as tk
from helpers.main_test_helpers import check_tk_exists, check_widget_props

#check if unicode search menu opens
def get_unicode_menu_build_test(root, FONTS, COLORS, WINDOWS): 
    panel_frame, is_panel_frame = check_tk_exists(root, "unicode_search_panel")

    #for all widgets within the search frame w/o names
    children = panel_frame.winfo_children() if is_panel_frame else[]


    title_label = next( 
        (w for w in children if isinstance(w, tk.Label)and w.cget("text") == "Unicode Symbol Search"), 
        None,
    )

    subtitle_label = next(
        (w for w in children if isinstance(w, tk.Label) and w.cget("text") == "Search for unicode symbols by name or codepoint"),
        None,
    )
    search_box = next((w for w in children if isinstance(w, tk.Entry)), None)
    results_frame = next((w for w in children if isinstance(w, tk.Frame)), None)

    #check if search menu's inner widget exists (future: to name each inner widgets)
    is_title_label = title_label is not None
    is_subtitle_label = subtitle_label is not None
    is_search_box = search_box is not None
    is_results_frame = results_frame is not None

    #panel_frame
    panel_frame_props = [ 
        ("config", "bg", COLORS["bg_main"]), 
        ("config", "padx", 20), 
        ("config", "pady", 20), 
        ("config", "takefocus", "1"),

        ("pack","side", "top"),
        ("pack", "fill", "both"),
        ("pack", "expand", True),

        ("misc", "widget_name", "unicode_search_panel"),
    ] 
    is_panel_frame_props = check_widget_props(panel_frame, panel_frame_props)
   
    #title_label
    title_label_prop= [ 
        ("config", "bg", COLORS["bg_main"]),
        ("config", "fg", COLORS["text_main"]),
        ("misc", "font", FONTS["font_title"].actual()),
        ("config", "text", "Unicode Symbol Search"),
        ("pack", "fill", "x"),
        ("pack", "pady", 0),
    ]
    is_title_label_props = check_widget_props(title_label, title_label_prop)

    #subtitle_label 
    subtitle_label_prop = [ 
        ("config", "fg", COLORS["text_muted"]), 
        ("config", "bg", COLORS["bg_main"]),
        ("config", "text", "Search for unicode symbols by name or codepoint"),
        ("pack", "fill", "x"),
        ("pack", "pady", (0,15)),
        ("misc", "font", FONTS["font_subtitle"].actual()),
    ]

    is_subtitle_label_props = check_widget_props(subtitle_label, subtitle_label_prop)

    #search_box
    search_box_prop = [ 
        ("config", "fg", COLORS["text_main"]), 
        ("config", "bg", COLORS["bg_input"]),
        ("config", "insertbackground", "white"), 
        ("config", "highlightbackground", COLORS["border"]), 
        ("config", "highlightthickness", 1), 
        ("config", "bd", 1),
        ("pack", "fill", "x"),
        ("pack", "ipady", 6),
        ("misc", "font", FONTS["font_subtitle"].actual()),
    ]
    is_search_box_props=check_widget_props(search_box,search_box_prop)

    #results_frame 
    results_frame_prop = [ 
        ("config", "bg", COLORS["bg_main"]), 
        ("pack", "fill", "both"), 
        ("pack", "expand", True),
        ("pack", "pady", (15,0)), 
    ]
    is_result_frame_props = check_widget_props(results_frame,results_frame_prop)

    #verify the toggling from latex window to unicode window destorys the previous 
    _, is_latex_frame_present = check_tk_exists(root, "latex_frame")
    is_latex_frame_destroyed = not is_latex_frame_present

    return { 
        "is_panel_frame": is_panel_frame, 
        "is_title_label": is_title_label, 
        "is_subtitle_label": is_subtitle_label, 
        "is_search_box": is_search_box, 
        "is_results_frame": is_results_frame, 
        "is_panel_frame_prop": is_panel_frame_props,
        "is_title_label_prop": is_title_label_props, 
        "is_subtitle_label_prop": is_subtitle_label_props, 
        "is_search_box_prop": is_search_box_props, 
        "is_results_frame_prop": is_result_frame_props, 
        "is_latex_frame_destroyed": is_latex_frame_destroyed,
    }

