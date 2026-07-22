import tkinter as tk 

import utils.unicode_search as unicode_search
import utils.shortcuts_unicode as shortcuts_unicode
import utils.settings as settings
import utils.auth as auth
import utils.templates as templates

_active_render = {"callback": None}

def _unsubscribe_active_render(): 
    callback = _active_render["callback"]
    if callback is not None: 
        shortcuts_unicode.unlist(callback)
        _active_render["callback"] = None

#keybind popup
def _bind_key(parent, symbol, name, COLORS, FONTS, on_select): 
    popup = tk.Toplevel(parent, bg = COLORS["bg_main"]) 
    popup.title("Bind symbol to key or phrase")
    popup.configure(padx=20, pady=20)
    popup.transient(parent)
    popup.grab_set()
    popup.resizable(False, False)

    popuptitle =tk.Label(popup, text=f"Bind a key or phrase to {symbol} {name}", bg = COLORS["bg_main"], fg = COLORS["text_main"], font=FONTS["font_title"])
    popuptitle.pack(pady=(0, 10))

    prompt = tk.Label(popup, text="Type an key/phrase, then press enter...", bg = COLORS["bg_main"], fg = COLORS["text_main"], font=FONTS["font_subtitle"])
    prompt.pack(pady=(0,8))

    alias = tk.StringVar()
    entry = tk.Entry(popup, textvariable=alias, bg=COLORS["bg_input"], fg=COLORS["text_main"], insertbackground="white", bd=1, highlightbackground=COLORS["border"], highlightthickness=1, font=FONTS["font_subtitle"])
    entry.pack(fill ="x", ipady=6)

    #tracks previous user input for confirmation (prevent overwrite)
    pending = {"input": None}

    #capture keystroke to bind
    def on_key_press(alias):
        raw_input = alias.get()
        if not raw_input.strip(): 
            return 
        
        #check input previous binds
        status, message = shortcuts_unicode.check_binding(raw_input, symbol)

        #invalid keys/reserved binds 
        if status == "error" or status == "protected": 
            pending["input"] = None
            prompt.config(text = message, font=FONTS["font_subtitle"], fg = "#FF0000")
            return 

        #warning for matched binds 
        if status == "conflict" and pending["input"] != raw_input: 
            #update the input after first enter
            pending["input"] = raw_input 
            prompt.config(text =f"{message} Press Enter again to overwrite. Esc to Cancel bind.", font = FONTS["font_subtitle"], fg = "#FFA500")
            return 
        
        #if users continues to overwrite/status is non-error 
        if status == "conflict": 
            overwrite = True 
        else: 
            overwrite = False
        
        template_name = settings.lookup_setting("curr_template")
        email, e = auth.get_email()

        ok_shortcut, shortcut_msg = shortcuts_unicode.set_unicode_binding(raw_input, symbol, overwrite = overwrite)
        ok_template = True 
        template_msg =""

        if email:
            bindings = shortcuts_unicode.all_bindings()
            ok_template,result = templates.update_template(email, template_name, bindings)
        else:
            ok_template = True
        if ok_shortcut and ok_template: 
            popup.destroy()
            on_select(result)
        else: 
            pending["input"] = None 
            prompt.config(text = result, font = FONTS["font_subtitle"], fg ="#FF0000")
        
    entry.bind("<Return>", lambda e: on_key_press(alias))
    popup.bind("<Escape>", lambda e: popup.destroy())
    entry.focus_force()

def _do_search(query, results_frame, COLORS, FONTS):
    _unsubscribe_active_render()

    #clear previous results
    for child in results_frame.winfo_children(): 
        child.destroy()

    results = unicode_search.search(query.get())

    # invalid results
    if not results: 
        empty = tk.Label(results_frame, text="No relevant symbols found. Check unicode codepoint", fg = COLORS["text_muted"], bg=COLORS["bg_main"],font=FONTS["font_subtitle"])
        empty.pack(fill="x", pady=10) 
        return 
    
    root = results_frame.winfo_toplevel()

    rows = {}

    def _render(): 
        for symbol, button in rows.items():
            if not button.winfo_exists(): 
                continue 
            label = shortcuts_unicode.binding_label(symbol)
            if label: 
                button.config(text=label, fg  = COLORS["accent_blue"])
            else: 
                button.config(text="bind", fg = COLORS["action_green"])

    # display valid inputs as rows 
    for ch, name, cp in results: 
        row = tk.Frame(results_frame, bg=COLORS["bg_input"])
        row.pack(fill="x",pady=2) 

        symbol_icon = tk.Label(row, text=ch, fg=COLORS["text_main"], bg=COLORS["bg_input"],font=FONTS["font_title"])
        symbol_icon.pack(side="left", padx=(8,4))

        symbol_info = tk.Label(row, text=f"{name} (U+{cp:04X})", fg=COLORS["text_muted"], bg=COLORS["bg_input"],font=FONTS["font_subtitle"], anchor="w")
        symbol_info.pack(side="left", fill='x', expand = True) 

        bind_button =tk.Button(row, text="bind", fg=COLORS["action_green"], bg=COLORS["bg_input"], font=FONTS["font_subtitle"], bd=0)           
        bind_button.config(command = lambda c=ch, n=name, b =bind_button: _bind_key(root, c, n, COLORS, FONTS, lambda msg: b.config(text=msg, fg=COLORS["accent_blue"])))
        bind_button.pack(side="right", padx=8)

        rows[ch] = bind_button

    shortcuts_unicode.refresh(_render)
    _active_render["callback"] = _render

    _render()


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

    def on_destroy(event): 
        if event.widgert is results_frame: 
            _unsubscribe_active_render() 
    
    results_frame.bind("<Destroy>", on_destroy)
# Destroy function to tear down unicode search panel
def destroy_unicode_search_panel(root):

    _unsubscribe_active_render()

    # Remove all child widgets except for the navbar
    for widget in root.winfo_children():
        if widget.winfo_name() != "navbar_frame":
          widget.destroy()