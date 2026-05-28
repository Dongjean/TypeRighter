import tkinter as tk 

import utils.unicode_search as unicode_search 

#keybind popup
def _bind_key(parent, symbol, name, COLORS, FONTS, on_select): 
    popup = tk.Toplevel(parent, bg = COLORS["bg_main"]) 
    popup.title("Bind symbol to key")
    popup.configure(padx=20, pady=20)
    popup.grab_set()
    popup.transient(parent)
    popup.resizable(False, False)

    popuptitle =tk.Label(popup, text=f"Bind a key to {symbol} {name}", bg = COLORS["bg_main"], fg = COLORS["text_main"], font=FONTS["font_title"])
    popuptitle.pack(pady=(0, 10))

    prompt = tk.Label(popup, text="Press any key ...", bg = COLORS["bg_main"], fg = COLORS["text_main"], font=FONTS["font_subtitle"])
    prompt.pack(pady=15)

    #capture keystroke to bind
    def on_key_press(event):
        if not event.char or not event.char.strip(): 
            return
        #call shortcut function
        ok, message = shortcut.set_binding(event.char, symbol)
        if ok: 
            popup.destroy()
            on_select(message)
        else:
            prompt.config(text=message, font=FONTS["font_subtitle"], fg="#FF0000")

    popup.bind("<Key>", on_key_press)
    popup.bind("<Escape>", lambda e: popup.destroy())
    popup.focus_set()

def _do_search(query, results_frame, COLORS, FONTS):
    #clear previous results
    for child in results_frame.winfo_children(): 
        child.destroy()

    results = unicode_search.search(query.get())

    # invalid results
    if not results: 
        empty = tk.Label(results_frame, text="No relevant symbols found. Check unicode codepoint", fg = COLORS["text_muted"], bg=COLORS["bg_main"],font=FONTS["font_subtitle"])
        empty.pack(fill="x", pady=10) 
        return 
    
    # display valid inputs as rows 
    for ch, name, cp in results: 
        row = tk.Frame(results_frame, bg=COLORS["bg_input"])
        row.pack(fill="x",pady=2) 

        symbol_icon = tk.Label(row, text=ch, fg=COLORS["text_main"], bg=COLORS["bg_input"],font=FONTS["font_title"])
        symbol_icon.pack(side="left", padx=(8,4))

        symbol_info = tk.Label(row, text=f"{name} (U+{cp:04X})", fg=COLORS["text_muted"], bg=COLORS["bg_input"],font=FONTS["font_subtitle"], anchor="w")
        symbol_info.pack(side="left", fill='x', expand = True) 

        bind_button =tk.Button(row, text="bind", fg=COLORS["action_green"], bg=COLORS["bg_input"], font=FONTS["font_subtitle"],
                               command=lambda ch=ch, name=name: _bind_key(row, ch, name, COLORS, FONTS, lambda msg: bind_button.config(text=msg, fg=COLORS["accent_blue"])))
        bind_button.pack(side="right", padx=8)

def build_unicode_search_panel(root, COLORS, FONTS):
    #frame that contains results frame 
    panel_frame =tk.Frame(root, bg= COLORS["bg_main"], padx=20, pady=20, takefocus=True, name ="unicode_search_panel")
    panel_frame.pack(side="top", fill="both", expand=True)

    #header 
    title_label = tk.Label(panel_frame, text="Unicode Symbol Search", fg=COLORS["text_main"], bg=COLORS["bg_main"], font=FONTS["font_title"])
    title_label.pack(fill="x", pady=0)
    
    subtitle_label = tk.Label(panel_frame, text="Search for unicode symbols by name or codepoint", fg=COLORS["text_muted"], bg=COLORS["bg_main"], font=FONTS["font_subtitle"])
    subtitle_label.pack(fill="x", pady=(0, 15))

    #Search box
    query = tk.StringVar()
    search_box = tk.Entry(panel_frame, textvariable=query, bg=COLORS["bg_input"], fg=COLORS["text_main"], insertbackground="white", bd=1, highlightbackground=COLORS["border"], highlightthickness=1, font=FONTS["font_subtitle"])
    search_box.pack(fill="x", ipady = 6)

    #Results frame
    results_frame = tk.Frame(panel_frame, bg=COLORS["bg_main"])
    results_frame.pack(fill="both", expand=True, pady=(15,0))  

    search_box.focus_set()

    #Listen and update for any changes
    def on_type(*_): 
        _do_search(query, results_frame, COLORS, FONTS)
        
    query.trace_add("write", on_type)
        
# Destroy function to tear down unicode search panel
def destroy_unicode_search_panel(root):

    # Remove all child widgets except for the navbar
    for widget in root.winfo_children():
        if widget.winfo_name() != "navbar_frame":
          widget.destroy()