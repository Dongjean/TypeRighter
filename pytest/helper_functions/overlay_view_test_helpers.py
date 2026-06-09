import sys
from pynput import keyboard

key_simulator = keyboard.Controller()

border_thickness = 5
def get_overlay_init_tests(root, sw, sh):

    # All of these should be True
    is_root = root != None
    is_overrideredirect = root.overrideredirect() == True
    is_topmost = root.attributes("-topmost") == True
    is_alpha = root.attributes("-alpha") == 0.5
    is_transparentcolor = False
    if sys.platform.startswith("win"):
        is_transparentcolor = str(root.attributes("-transparentcolor")) == "white"
    elif sys.platform.startswith("linux"):
        # Just skip the test by letting it pass
        is_transparentcolor = True
    else:
        is_transparentcolor = str(root.attributes("-transparentcolor")) == "white"
    is_geometry = root.geometry() == f"{sw}x{sh}+0+0"

    # Check the canvas' properties in the overlay that we set
    # We tagged the canvas that we made with "overlay"
    canvas = root.nametowidget(".overlay")
    is_canvas = canvas != None
    is_bg = canvas.cget("bg") == "white"
    is_highlightthickness = canvas.cget("highlightthickness") == "0"
    is_fill = canvas.pack_info().get("fill") == "both"
    is_expand = canvas.pack_info().get("expand") == True

    canvas_rectangle_id = canvas.find_withtag("overlay")[0]
    is_rectangle = canvas.type(canvas_rectangle_id) == "rectangle"
    is_coords = canvas.coords("overlay") == [border_thickness//2, border_thickness//2, sw - border_thickness//2, sh - border_thickness//2]
    is_outline = canvas.itemcget("overlay", "outline") == "green"
    is_width = float(canvas.itemcget("overlay", "width")) == border_thickness
    is_fill = canvas.itemcget("overlay", "fill") == "white"

    return {
        "is_root": is_root,
        "is_overrideredirect": is_overrideredirect,
        "is_topmost": is_topmost,
        "is_alpha": is_alpha,
        "is_transparentcolor": is_transparentcolor,
        "is_geometry": is_geometry,

        "is_canvas": is_canvas,
        "is_bg": is_bg,
        "is_highlightthickness": is_highlightthickness,
        "is_fill": is_fill,
        "is_expand": is_expand,

        "is_rectangle": is_rectangle,
        "is_coords": is_coords,
        "is_outline": is_outline,
        "is_width": is_width,
        "is_fill": is_fill
    }
