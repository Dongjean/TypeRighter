from helper_functions.main_test_helpers import check_tk_exists, check_widget_props

def get_latex_build_tests(root, FONTS, COLORS):

    # Check if all the widgets exist
    latex_frame, is_latex_frame = check_tk_exists(root, "latex_frame")
    title_label, is_title_label = check_tk_exists(latex_frame, "title_label")
    subtitle_label, is_subtitle_label = check_tk_exists(latex_frame, "subtitle_label")
    editor_container, is_editor_container = check_tk_exists(latex_frame, "editor_container")
    text_editor, is_text_editor = check_tk_exists(editor_container, "text_editor")
    latex_output_container, is_latex_output_container = check_tk_exists(latex_frame, "latex_output_container")
    preview_label, is_preview_label = check_tk_exists(latex_output_container, "preview_label")
    latex_output_canvas, is_latex_output_canvas = check_tk_exists(preview_label, "latex_output_canvas")
    compile_button, is_compile_button = check_tk_exists(editor_container, "compile_button")

    # Check the properties of each widget

    # latex_frame
    # Get our desired latex_frame_props
    latex_frame_props = [
        ("config", "bg", COLORS["bg_main"]),
        ("config", "padx", 20),
        ("config", "pady", 20),
        ("config", "takefocus", "1"),

        ("pack", "side", "top"),
        ("pack", "fill", "both"),
        ("pack", "expand", True),

        ("misc", "widget_name", "latex_frame")
    ]
    is_latex_frame_props = check_widget_props(latex_frame, latex_frame_props)

    # title_label
    title_label_props = [
        ("config", "text", "LaTeX Equation Editor"),
        ("config", "bg", COLORS["bg_main"]),
        ("config", "fg", COLORS["text_main"]),

        ("pack", "fill", "x"),
        ("pack", "pady", 0),

        ("misc", "widget_name", "title_label"),

        ("misc", "font", FONTS["font_title"].actual())
    ]
    is_title_label_props = check_widget_props(title_label, title_label_props)

    # subtitle_label
    subtitle_label_props = [
        ("config", "text", "Edit and preview complex mathematical formulas"),
        ("config", "bg", COLORS["bg_main"]),
        ("config", "fg", COLORS["text_muted"]),

        ("pack", "fill", "x"),
        ("pack", "pady", (0, 15)),

        ("misc", "widget_name", "subtitle_label"),

        ("misc", "font", FONTS["font_subtitle"].actual())
    ]
    is_subtitle_label_props = check_widget_props(subtitle_label, subtitle_label_props)

    # editor_container
    editor_container_props = [
        ("config", "bg", COLORS["bg_input"]),
        ("config", "bd", 1),
        ("config", "highlightbackground", COLORS["border"]),
        ("config", "highlightthickness", 1),

        ("pack", "fill", "both"),
        ("pack", "expand", True),

        ("misc", "widget_name", "editor_container"),
    ]
    is_editor_container_props = check_widget_props(editor_container, editor_container_props)

    # text_editor
    text_editor_props = [
        ("config", "bg", COLORS["bg_input"]),
        ("config", "fg", COLORS["text_main"]),
        ("config", "insertbackground", "white"),
        ("config", "bd", 0),
        ("config", "padx", 15),
        ("config", "pady", 15),
        ("config", "wrap", "none"),

        ("pack", "fill", "both"),
        ("pack", "expand", True),

        ("misc", "widget_name", "text_editor"),

        ("misc", "font", FONTS["font_subtitle"].actual()),

        ("misc", "bind", "<Key-Return>"),
        ("misc", "bind", "<Shift-Key-Return>")
    ]
    is_text_editor_props = check_widget_props(text_editor, text_editor_props)

    # latex_output_container
    latex_output_container_props = [
        ("config", "bg", COLORS["bg_input"]),
        ("config", "bd", 1),
        ("config", "highlightbackground", COLORS["border"]),
        ("config", "highlightthickness", 1),
        ("config", "height", 150),

        ("pack", "fill", "x"),
        ("pack", "pady", (5, 20)),

        ("misc", "widget_name", "latex_output_container"),

        ("misc", "pack_propagate", False)
    ]
    is_latex_output_container_props = check_widget_props(latex_output_container, latex_output_container_props)

    # preview_label
    preview_label_props = [
        ("config", "bg", "white"),

        ("pack", "fill", "both"),
        ("pack", "expand", True),

        ("misc", "widget_name", "preview_label")
    ]
    is_preview_label_props = check_widget_props(preview_label, preview_label_props)

    # latex_output_canvas
    latex_output_canvas_props = [
        ("config", "bg", "white"),
        ("config", "highlightthickness", "0"),

        ("pack", "expand", True),

        ("misc", "widget_name", "latex_output_canvas")
    ]
    is_latex_output_canvas_props = check_widget_props(latex_output_canvas, latex_output_canvas_props)

    # compile_button
    compile_button_props = [
        ("config", "text", "Compile"),
        ("config", "bg", COLORS["border"]),
        ("config", "fg", COLORS["text_main"]),
        ("config", "bd", 0),
        ("config", "relief", "flat"),
        ("config", "command", True), # Check that a function is linked to command

        ("pack", "side", "right"),

        ("misc", "widget_name", "compile_button"),

        ("misc", "font", FONTS["font_subtitle"].actual())
    ]
    is_compile_button_props = check_widget_props(compile_button, compile_button_props)

    # root
    root_props = [
        ("misc", "bind", "<Key-Return>"),
        ("misc", "bind", "<Shift-Key-Return>")
    ]
    is_root_props = check_widget_props(root, root_props)

    return {
        "is_latex_frame": is_latex_frame,
        "is_title_label": is_title_label,
        "is_subtitle_label": is_subtitle_label,
        "is_editor_container": is_editor_container,
        "is_text_editor": is_text_editor,
        "is_latex_output_container": is_latex_output_container,
        "is_preview_label": is_preview_label,
        "is_latex_output_canvas": is_latex_output_canvas,
        "is_compile_button": is_compile_button,
        "is_latex_frame_props": is_latex_frame_props,
        "is_title_label_props": is_title_label_props,
        "is_subtitle_label_props": is_subtitle_label_props,
        "is_editor_container_props": is_editor_container_props,
        "is_text_editor_props": is_text_editor_props,
        "is_latex_output_container_properties": is_latex_output_container_props,
        "is_preview_label_props": is_preview_label_props,
        "is_latex_output_canvas_props": is_latex_output_canvas_props,
        "is_compile_button_props": is_compile_button_props,
        "is_root_props": is_root_props
    }
