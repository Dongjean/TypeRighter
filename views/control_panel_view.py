def control_panel_init(root):
    root.title("TypeRighter - Control Panel")

    # Manually reset all of the settings from root_init()
    root.overrideredirect(False)
    root.attributes("-topmost", False)
    root.attributes("-alpha", 1.0)
    root.attributes("-transparentcolor", "") # Clear the transparent color mask

    root.geometry("800x600+200+200")

    # Get the canvas and delete it
    canvas = root.children["overlay"]
    canvas.destroy()

    # Force refresh the tkinter window by processing all the idle tasks
    # Note: the .geometry() line being before this MAY cause problems later
    root.update_idletasks()
    root.focus_force()
