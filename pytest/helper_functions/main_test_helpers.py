import time
from tkinter import font as tkfont

# Helper function to pause the programme for a short few seconds while spamming root.update()
def wait(root, period, interval=0.05):
    deadline = time.time() + period
    while time.time() < deadline:
        root.update()
        time.sleep(interval)

def check_tk_exists(parent, child_name):
    try:

        # Widget with name child_name exists under the widget parent
        child_widget = parent.nametowidget(child_name)
        return (child_widget, True)
    except KeyError:

        # Widget with name child_name does not exist under the widget parent
        return (None, False)
    except AttributeError:

        # The widget parent doesnt exist
        return (None, False)

def check_widget_props(widget, props):
    widget_pack_info = None
    widget_place_info = None
    widget_binds = None
    try:
        widget_pack_info = widget.pack_info()
    except AttributeError as e:
        print(e)
    except Exception as e:
        print(e)
    try:
        widget_place_info = widget.place_info()
    except AttributeError as e:
        print(e)
    try:
        widget_binds = widget.bind()
    except AttributeError as e:
        print(e)
    curr_props = [

        # Command prop (Check that the function exists only)
        (prop[0], prop[1], True if widget.cget(prop[1]) else False) if prop[0] == "config" and prop[1] == "command"
        else
        # variable prop (for RadioButton)
        (prop[0], prop[1], str(widget.cget(prop[1]))) if prop[0] == "config" and prop[1] == "variable"
        else
        # Config props
        (prop[0], prop[1], widget.cget(prop[1])) if prop[0] == "config"
        else
        # Pack props
        (prop[0], prop[1], widget_pack_info[prop[1]]) if prop[0] == "pack"
        else
        # Place props
        (prop[0], prop[1], widget_place_info[prop[1]]) if prop[0] == "place"
        else
        # Widget name prop
        (prop[0], prop[1], widget.winfo_name()) if prop[0] == "misc" and prop[1] == "widget_name"
        else
        # Font prop
        (prop[0], prop[1], tkfont.nametofont(widget.cget("font")).actual()) if prop[0] == "misc" and prop[1] == "font"
        else
        # pack_propagate prop
        (prop[0], prop[1], widget.tk.call('pack', 'propagate', widget._w)) if prop[0] == "misc" and prop[1] == "pack_propagate"
        else
        # Bind prop
        (prop[0], prop[1], prop[2] if prop[2] in widget_binds else None) if prop[0] == "misc" and prop[1] == "bind"
        else
        # Python syntax demands a fallback
        (prop[0], prop[1], prop[2])
        for prop in props
    ]
    print(curr_props)
    is_widget_props = all([
        curr_props[index] == prop for index, prop in enumerate(props)
    ])
    
    return is_widget_props