import sys

from helper_functions.main_test_helpers import check_widget_props

def get_cp_init_tests(root, sw, sh):

    # All of these should be True

    is_root = root != None
    is_title = root.title() == "TypeRighter - Control Panel"

    # There is a known bug with tkinter, where root.overrideredirect() == None when we set it to False
    # This is because setting it to False gives control of the title bar and borders to the native OS
    # The windows OS returns 0, but for some reason tkinter's internal boolean converters converts that to None
    is_overrideredirect = root.overrideredirect() == None
    is_topmost = root.attributes("-topmost") == False
    is_alpha = root.attributes("-alpha") == 1
    is_transparentcolor = False
    if sys.platform.startswith("win"):
        is_transparentcolor = str(root.attributes("-transparentcolor")) == ""
    elif sys.platform.startswith("linux"):
        # Just skip the test by letting it pass
        is_transparentcolor = True
    else:
        is_transparentcolor = str(root.attributes("-transparentcolor")) == ""
    is_geometry = root.geometry() == f"{sw // 2}x{sh // 2}+0+0"
    is_bg_white = root.cget("bg") == "#ffffff"

    # Check that there is no overlay canvas anymore
    is_overlay_gone = False
    try:
        # Try to access the overlay_canvas
        root.nametowidget(".overlay")
    except KeyError:
        # If we cannot find it because any child widget with the name "overlay" cannot be found, then overlay is truly gone
        is_overlay_gone = True

    # Check that it is not withdrawn
    is_deiconify = root.state() == "normal"

    # Check that we have the root keybind to <Button-1>
    is_root_bind = check_widget_props(root, [("misc", "bind", "<Button-1>")])

    return {
        "is_root": is_root,
        "is_title": is_title,
        "is_overrideredirect": is_overrideredirect,
        "is_topmost": is_topmost,
        "is_alpha": is_alpha,
        "is_transparentcolor": is_transparentcolor,
        "is_geometry": is_geometry,
        "is_bg_white": is_bg_white,

        "is_overlay_gone": is_overlay_gone,

        "is_deiconify": is_deiconify,

        "is_root_bind": is_root_bind
    }