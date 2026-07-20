import tkinter as tk
from tkinter import ttk

import utils.shortcuts_unicode as shortcuts_unicode
import utils.settings as settings
import main as main
import views.view_handler as view_handler
import utils.auth as auth
import utils.templates as templates

import components.navbar as navbar

PROTECTED_BINDS = ["Exit App", "Close Overlay", "Control Panel", "Breakout Key"]

def toggle_binds_expansion(binds_container, label):
    
    # Get the text property of the label, without the trailing ▲▼
    text = label["text"][:-1]
    print(text)
    print(binds_container)
    print(label)
    # If the widget is already visible, turn it off
    if binds_container.winfo_ismapped():
        binds_container.pack_forget()
        text += "▼"
    else:
        binds_container.pack()
        text += "▲"
    
    # Update the label
    label.configure(text=text)

def _refresh_keybinds(keybinds_display_container, preferences_frame, COLORS, FONTS):
    
    # Get the new keybinds
    curr_keybinds = shortcuts_unicode.all_key_bindings()
    print(curr_keybinds)
    # First Delete Existing Keybinds
    for widget in keybinds_display_container.winfo_children():
        widget.destroy()

    # Then Create the new Keybinds
    for key, bind in curr_keybinds.items():

        # This Keybind's Container
        keybind_container = tk.Frame(keybinds_display_container, bg=COLORS["bg_input"], name=f"{key}_keybind_container")
        keybind_container.pack(pady=2, anchor="w")

        # The Key Label
        key_label = tk.Label(keybind_container, bg=COLORS["bg_input"], font=FONTS["font_subtitle"], highlightbackground="white", highlightthickness=1, fg=COLORS["text_main"], text=key, name=f"{key}_key_label")
        key_label.pack(side="left")

        # The Corresponding Bind Label
        bind_label = tk.Label(keybind_container, bg=COLORS["bg_input"], font=FONTS["font_subtitle"], fg=COLORS["text_main"], text=bind, name=f"{key}_bind_label")
        bind_label.pack(side="left")

        # This Keybind's Unbinder
        # Display this iff it isnt one of the protected keys
        if bind not in ["Exit App", "Close Overlay", "Control Panel", "Breakout Key"]:
            keybind_unbinder = tk.Button(keybind_container, text="Unbind", fg=COLORS["action_green"], bg=COLORS["bg_input"], font=FONTS["font_subtitle"], bd=0, command=lambda COLORS=COLORS, FONTS=FONTS, key=key: _unbind_key(keybinds_display_container, preferences_frame, COLORS, FONTS, key), name=f"{key}_keybind_unbinder")
            keybind_unbinder.pack(side="right", padx=8)

        # This Keybind's Rebinder
        keybind_rebinder = tk.Button(keybind_container, text="Rebind", fg=COLORS["action_green"], bg=COLORS["bg_input"], font=FONTS["font_subtitle"], bd=0, command = lambda to_bind=bind, old_key=key: _rebind_key(preferences_frame, to_bind, old_key, COLORS, FONTS), name=f"{key}_keybind_rebinder")
        keybind_rebinder.pack(side="right")

# Keybind popup
def _rebind_key(parent, to_bind, old_key, COLORS, FONTS): 
    popup = tk.Toplevel(parent, bg = COLORS["bg_main"]) 
    popup.title("Bind symbol to key or phrase")
    popup.configure(padx=20, pady=20)
    popup.transient(parent)
    popup.grab_set()
    popup.resizable(False, False)

    popuptitle = tk.Label(popup, text=f"Re-bind a key to {to_bind}", bg = COLORS["bg_main"], fg = COLORS["text_main"], font=FONTS["font_title"])
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
        new_key = alias.get()
        if not new_key.strip(): 
            return 
        
        #check input previous binds
        status, message = shortcuts_unicode.check_binding(new_key, to_bind)

        #invalid keys/reserved binds 
        if status == "error" or status == "protected": 
            pending["input"] = None
            prompt.config(text = message, font=FONTS["font_subtitle"], fg = "#FF0000")
            return 

        #warning for matched binds 
        if status == "conflict" and pending["input"] != new_key: 
            #update the input after first enter
            pending["input"] = new_key 
            prompt.config(text =f"{message} Press Enter again to overwrite. Esc to Cancel bind.", font = FONTS["font_subtitle"], fg = "#FFA500")
            return 
        
        #if users continues to overwrite/status is non-error 
        if status == "conflict": 
            overwrite = True 
        else: 
            overwrite = False
        
        template_name = settings.lookup_setting("curr_template")
        email, e = auth.get_email()
        ok_shortcut,result = shortcuts_unicode.set_unicode_binding(new_key, to_bind, overwrite = overwrite)
        if email:
            bindings = shortcuts_unicode.all_bindings()
            ok_template,result = templates.update_template(email, template_name, bindings)
        else:
            ok_template = True
        if ok_shortcut and ok_template: 
            popup.destroy()
            shortcuts_unicode.remove_unicode_binding(old_key)
            if email:
                templates.update_template(email, template_name, bindings)
            _refresh_both(parent, COLORS, FONTS)
            if new_key.lower() != old_key.lower(): 
                shortcuts_unicode.remove_unicode_binding(old_key)
                if email:
                    templates.update_template(email, template_name, bindings)
            if to_bind == "Breakout Key":
                print("updating")
                main.update_breakout_key()
        else: 
            pending["input"] = None 
            prompt.config(text = result, font = FONTS["font_subtitle"], fg ="#FF0000")
        
    entry.bind("<Return>", lambda e: on_key_press(alias))
    popup.bind("<Escape>", lambda e: popup.destroy())
    entry.focus_force()

def _unbind_key(keybinds_display_container, preferences_frame, COLORS, FONTS, key):
    
    template_name = settings.lookup_setting("curr_template")
    email, e = auth.get_email()
    shortcuts_unicode.remove_unicode_binding(key)
    if email:
        bindings = shortcuts_unicode.all_bindings()
        templates.update_template(email, template_name, bindings)
    _refresh_both(preferences_frame, COLORS, FONTS)

def _refresh_phrasebinds(phrasebind_display_container, preferences_frame,COLORS, FONTS):

    #get current phrase binds 
    curr_phrase_shortcuts = shortcuts_unicode.all_phrase_bindings()

    for widget in phrasebind_display_container.winfo_children(): 
        widget.destroy()

    #show each phrase binds 
    for phrase, bind in curr_phrase_shortcuts.items(): 

        phrasebind_container = tk.Frame(phrasebind_display_container, bg = COLORS["bg_input"], name = f"{phrase}_phrasebind_container")
        phrasebind_container.pack(pady=2, anchor ="w")

        phrase_label = tk.Label(phrasebind_container, bg = COLORS["bg_input"], font = FONTS["font_subtitle"], highlightbackground = "white", highlightthickness = 1, fg = COLORS["text_main"], text = phrase, name =f"{phrase}_phrase_label")
        phrase_label.pack(side ="left")

        bind_label = tk.Label(phrasebind_container, bg = COLORS["bg_input"], font = FONTS["font_subtitle"], fg = COLORS["text_main"], text = bind, name =f"{phrase}_bind_label")
        bind_label.pack(side ="left")

                # This Keybind's Unbinder
        # Display this iff it isnt one of the protected keys
        if bind not in PROTECTED_BINDS:
            phrasebind_unbinder = tk.Button(phrasebind_container, text="Unbind", fg=COLORS["action_green"], bg=COLORS["bg_input"], font=FONTS["font_subtitle"], bd=0, command=lambda phrase = phrase: _unbind_phrase(phrasebind_display_container, preferences_frame, COLORS, FONTS, phrase), name=f"{phrase}_phrasebind_unbinder")
            phrasebind_unbinder.pack(side="right", padx=8)
            
        phrasebind_rebinder = tk.Button(phrasebind_container, text="Rebind", fg=COLORS["action_green"], bg=COLORS["bg_input"], font = FONTS["font_subtitle"], bd = 0, command = lambda to_bind=bind, old_key=phrase: _rebind_key(preferences_frame, to_bind, old_key, COLORS, FONTS), name = f"{phrase}_phrasebind_rebinder")
        phrasebind_rebinder.pack(side ="right")

def _unbind_phrase(phrasebind_display_container, preference_frame, COLORS, FONTS, phrase): 
    
    template_name = settings.lookup_setting("curr_template")
    email, e = auth.get_email()
    shortcuts_unicode.remove_unicode_binding(phrase)
    if email:
        bindings = shortcuts_unicode.all_bindings()
        templates.update_template(email, template_name, bindings)
    _refresh_both(preference_frame, COLORS, FONTS)
    
def _refresh_both(preferences_frame, COLORS, FONTS): 
    _refresh_keybinds(preferences_frame.keybinds_display_container, preferences_frame, COLORS, FONTS)
    _refresh_phrasebinds(preferences_frame.phrasebinds_display_container, preferences_frame, COLORS, FONTS)


        
def _refresh_latex_shortcuts(latex_shortcuts_display_container, preferences_frame, COLORS, FONTS):
    
    # Get the new keybinds
    curr_latex_shortcuts = shortcuts_unicode.all_latex_shortcuts()
    # First Delete Existing Keybinds
    for widget in latex_shortcuts_display_container.winfo_children():
        widget.destroy()

    # Show Each LaTeX Shortcut
    for key, latex_shortcut in curr_latex_shortcuts.items():
        
        # This LaTeX Shortcut's Container
        latex_shortcut_container = tk.Frame(latex_shortcuts_display_container, bg=COLORS["bg_input"], name=f"{key}_latex_shortcut_container")
        latex_shortcut_container.pack()

        # The LaTeX Shortcut Label
        latex_shortcut_label = tk.Label(latex_shortcut_container, bg=COLORS["bg_input"], font=FONTS["font_subtitle"], highlightbackground="white", highlightthickness=1, fg=COLORS["text_main"], text=latex_shortcut["name"], name=f"{key}_latex_shortcut_label")
        latex_shortcut_label.pack(side="left")

        # The Corresponding LaTeX Code Label
        latex_code_label = tk.Label(latex_shortcut_container, bg=COLORS["bg_input"], font=FONTS["font_subtitle"], fg=COLORS["text_main"], text=latex_shortcut["code"], name=f"{key}_latex_code_label")
        latex_code_label.pack(side="left")

        # This LaTeX Shortcut's Unbinder
        latex_shortcut_unbinder =tk.Button(latex_shortcut_container, text="Unbind", fg=COLORS["action_green"], bg=COLORS["bg_input"], font=FONTS["font_subtitle"], bd=0, command=lambda COLORS=COLORS, FONTS=FONTS, key=key: _unbind_latex_shortcut(latex_shortcuts_display_container, preferences_frame, COLORS, FONTS, key), name=f"{key}_latex_shortcut_unbinder")
        latex_shortcut_unbinder.pack(side="right", padx=8)

def _unbind_latex_shortcut(latex_shortcuts_display_container, preferences_frame, COLORS, FONTS, key):
    
    template_name = settings.lookup_setting("curr_template")
    email, e = auth.get_email()
    shortcuts_unicode.remove_latex_shortcut(key)
    if email:
        bindings = shortcuts_unicode.all_bindings()
        templates.update_template(email, template_name, bindings)
    _refresh_latex_shortcuts(latex_shortcuts_display_container, preferences_frame, COLORS, FONTS)

def add_latex_shortcut(latex_shortcut_adder_name_entry, latex_shortcut_adder_code_entry, latex_shortcut_adder_error_msg, latex_shortcuts_display_container, preferences_frame, COLORS, FONTS):
    
    # Get all text minus the auto-added trailing newline
    latex_name = latex_shortcut_adder_name_entry.get()
    latex_code = latex_shortcut_adder_code_entry.get("1.0", "end-1c")

    template_name = settings.lookup_setting("curr_template")
    email, e = auth.get_email()
    ok_shortcut, message = shortcuts_unicode.set_latex_shortcut(latex_code, latex_name)
    if email:
        bindings = shortcuts_unicode.all_bindings()
        ok_template,result = templates.update_template(email, template_name, bindings)
    else:
        ok_template = True
    if ok_shortcut and ok_template:

        # Clear the Entries
        latex_shortcut_adder_name_entry.delete(0, 'end')
        # Multi-line Code Entry
        latex_shortcut_adder_code_entry.delete('1.0', 'end')

        # Refresh the LaTeX Shortcuts Display
        _refresh_latex_shortcuts(latex_shortcuts_display_container, preferences_frame, COLORS, FONTS)
    else:
        latex_shortcut_adder_error_msg.config(text=message, fg="#FF0000")

def on_template_selection(event, template_selector, preferences_frame, COLORS, FONTS):
    
    # Get the current value from the combobox
    selected_template = template_selector.get()
    
    if selected_template:
        templates.use_template(selected_template)
        curr_user, e = auth.get_email()
        settings.set_setting("curr_template", selected_template, curr_user)
        shortcuts_unicode.load()
        main.update_breakout_key()
        _refresh_both(preferences_frame, COLORS, FONTS)

def edit_template_name(template_selector_hub, template_editor_hub):
        
    template_selector = template_selector_hub.nametowidget("template_selector")
    selected_template = template_selector.get()
    template_selector_hub.pack_forget()

    template_editor_hub.pack(fill="x", anchor="center")
    template_name_editor = template_editor_hub.nametowidget("template_name_editor")
    template_name_editor.delete(0, "end")
    template_name_editor.insert(0, selected_template)

def commit_template_name(template_selector_hub, template_editor_hub, template_name_editor, template_selector):
        
    email, e = auth.get_email()
    curr_selected_template = settings.lookup_setting("curr_template")
    new_template_name = template_name_editor.get()

    template_editor_hub.pack_forget()

    template_selector_hub.pack(fill="x", anchor="center")

    templates_ok, templates_e = templates.rename_template(email, curr_selected_template, new_template_name)

    settings_ok, settings_e = settings.set_setting("curr_template", new_template_name, email)

    print(templates_e)
    print(settings_e)

    # Update the template selectors
    curr_templates = templates.all_templates(email)
    curr_template_names = list(curr_templates)
    print(curr_template_names)
    template_selector.configure(values=curr_template_names)
    template_selector.set(new_template_name)

    # Update the Navbar's template selector
    # First get the root window
    root = template_selector.winfo_toplevel()
    navbar_frame = root.nametowidget("navbar_frame")
    navbar_template_selector = navbar_frame.nametowidget("template_selector")

    navbar_template_selector.configure(values=curr_template_names)
    navbar_template_selector.set(new_template_name)

def add_new_template(template_selector_hub, template_editor_hub):

    email, e = auth.get_email()
    new_template_name = templates.add_new_template(email)
    templates.use_template(new_template_name)
    settings.set_setting("curr_template", new_template_name, email)
    shortcuts_unicode.load()
    main.update_breakout_key()

    template_selector = template_selector_hub.nametowidget("template_selector")
    template_selector.set(new_template_name)

    # Automatically Enter Edit Template Name Mode
    edit_template_name(template_selector_hub, template_editor_hub)

def build_preferences_setting(settings_subwindow_container, COLORS, FONTS):
    
    # Preferences Frame
    preferences_frame = tk.Frame(settings_subwindow_container, bg=COLORS["bg_input"], takefocus=True, name="preferences_frame")
    preferences_frame.pack(expand=True)
    
    # Check if the user is logged in
    email, e = auth.get_email()
    if email:
        print(f"Displaying templates for user: {email}")
        # List of templates
        curr_templates = templates.all_templates(email)
        curr_template_names = list(curr_templates)

        # Templates Selector Container
        template_selector_container = tk.Frame(preferences_frame, bg=COLORS["bg_input"], name="template_selector_container")
        template_selector_container.pack(fill="x", anchor="center")

        # Templates Selector Hub
        template_selector_hub = tk.Frame(template_selector_container, bg=COLORS["bg_input"], name="template_selector_hub")
        template_selector_hub.pack(fill="x", anchor="center")

        # Templates Selector Label
        template_selector_label = tk.Label(template_selector_hub, bg=COLORS["bg_input"], font=FONTS["font_subtitle"], fg=COLORS["text_main"], text="Selected Template", name="template_selector_label")
        template_selector_label.pack()

        # Template Selector Dropdown Menu
        template_selector = ttk.Combobox(template_selector_hub, values=curr_template_names, state="readonly", name="template_selector")
        curr_selected_template = settings.lookup_setting("curr_template")
        template_selector.set(curr_selected_template)
        template_selector.bind("<<ComboboxSelected>>", lambda event: on_template_selection(event, template_selector, preferences_frame, COLORS, FONTS))
        template_selector.pack(side="left")

        # Change Template Name Button
        edit_template_name_button = tk.Label(template_selector_hub, text="Edit", bg=COLORS["bg_input"], font=FONTS["font_subtitle"], fg=COLORS["accent_blue"], name="edit_template_name_button")
        edit_template_name_button.bind("<Button-1>", lambda e: edit_template_name(template_selector_hub, template_editor_hub))
        edit_template_name_button.pack(side="left")

        # Add New Template Button
        new_template_button = tk.Label(template_selector_hub, text="+", bg=COLORS["bg_input"], font=FONTS["font_subtitle"], fg=COLORS["action_green"], name="new_template_button")
        new_template_button.bind("<Button-1>", lambda e: add_new_template(template_selector_hub, template_editor_hub))
        new_template_button.pack(side="left")

        # Templates Editor Hub
        template_editor_hub = tk.Frame(template_selector_container, bg=COLORS["bg_input"], name="template_editor_hub")
        
        # Template Editor Label
        template_editor_label = tk.Label(template_editor_hub, bg=COLORS["bg_input"], font=FONTS["font_subtitle"], fg=COLORS["text_main"], text="Edit Template Name", name="template_editor_label")
        template_editor_label.pack()

        # Template Name Editor Field
        template_name_editor = tk.Entry(template_editor_hub, name="template_name_editor")
        template_name_editor.pack(side="left")

        # Commit Edits Button
        commit_edits_button = tk.Label(template_editor_hub, text="Confirm Changes", bg=COLORS["bg_input"], font=FONTS["font_subtitle"], fg=COLORS["action_green"], name="commit_edits_button")
        commit_edits_button.bind("<Button-1>", lambda e: commit_template_name(template_selector_hub, template_editor_hub, template_name_editor, template_selector))
        commit_edits_button.pack(side="left")

    else:
        print(f"error initialising login state: {e}")

    # Display the Keybinds Under the Selected Template
    
    # Current Keybinds Container
    keybinds_container = tk.Frame(preferences_frame, bg=COLORS["bg_input"], name="curr_keybinds_container")
    keybinds_container.pack()
    
    # Keybinds Label
    keybinds_label = tk.Label(keybinds_container, bg=COLORS["bg_input"], font=FONTS["font_subtitle"], fg=COLORS["text_main"], text="Current Keybinds ▼", name="keybinds_label")
    keybinds_label.pack()
            
    keybinds_display_container = tk.Frame(keybinds_container, bg=COLORS["bg_input"], name="keybinds_display_container")

    preferences_frame.keybinds_display_container = keybinds_display_container

    _refresh_keybinds(keybinds_display_container, preferences_frame, COLORS, FONTS)

    keybinds_label.bind("<Button-1>", lambda e: toggle_binds_expansion(keybinds_display_container,keybinds_label))

    phrasebinds_container = tk.Frame(preferences_frame, bg= COLORS["bg_input"], name ="phrasebinds_container")
    phrasebinds_container.pack()

    phrasebinds_label = tk.Label(phrasebinds_container, bg= COLORS["bg_input"], font= FONTS ["font_subtitle"], fg= COLORS["text_main"], text = "Current Phrase Bindings  ▼", name ="phrasebinds_label")
    phrasebinds_label.pack()

    phrasebinds_display_container = tk.Frame(phrasebinds_container, bg = COLORS["bg_input"], name = "phrasebinds_display_container")

    preferences_frame.phrasebinds_display_container = phrasebinds_display_container

    #populate the phrase binding lists 
    _refresh_phrasebinds(phrasebinds_display_container, preferences_frame, COLORS, FONTS)

    phrasebinds_label.bind("<Button-1>", lambda e: toggle_binds_expansion(phrasebinds_display_container, phrasebinds_label))

    latex_shortcuts_container = tk.Frame(preferences_frame, bg=COLORS["bg_input"], name="latex_shortcuts_container")
    latex_shortcuts_container.pack()

    # LaTeX Shortcut Label
    latex_shortcuts_label = tk.Label(latex_shortcuts_container, bg=COLORS["bg_input"], font=FONTS["font_subtitle"], fg=COLORS["text_main"], text="Current LaTeX Shortcuts ▼", name="latex_shortcuts_label")
    latex_shortcuts_label.pack()

    # Get the list of all latex shortcuts
    curr_latex_shortcuts = shortcuts_unicode.all_latex_shortcuts()

    latex_shortcuts_display_container = tk.Frame(latex_shortcuts_container, bg=COLORS["bg_input"], name="latex_shortcuts_display_container")

    # Show Each LaTeX Shortcut
    for key, latex_shortcut in curr_latex_shortcuts.items():
        
        # This LaTeX Shortcut's Container
        latex_shortcut_container = tk.Frame(latex_shortcuts_display_container, bg=COLORS["bg_input"], name=f"{key}_latex_shortcut_container")
        latex_shortcut_container.pack()

        # The LaTeX Shortcut Label
        latex_shortcut_label = tk.Label(latex_shortcut_container, bg=COLORS["bg_input"], font=FONTS["font_subtitle"], highlightbackground="white", highlightthickness=1, fg=COLORS["text_main"], text=latex_shortcut["name"], name=f"{key}_latex_shortcut_label")
        latex_shortcut_label.pack(side="left")

        # The Corresponding LaTeX Code Label
        latex_code_label = tk.Label(latex_shortcut_container, bg=COLORS["bg_input"], font=FONTS["font_subtitle"], fg=COLORS["text_main"], text=latex_shortcut["code"], name=f"{key}_latex_code_label")
        latex_code_label.pack(side="left")

        # This LaTeX Shortcut's Unbinder
        latex_shortcut_unbinder =tk.Button(latex_shortcut_container, text="Unbind", fg=COLORS["action_green"], bg=COLORS["bg_input"], font=FONTS["font_subtitle"], bd=0, command=lambda COLORS=COLORS, FONTS=FONTS, key=key: _unbind_latex_shortcut(latex_shortcuts_display_container, preferences_frame, COLORS, FONTS, key), name=f"{key}_latex_shortcut_unbinder")
        latex_shortcut_unbinder.pack(side="right", padx=8)
    
    latex_shortcuts_label.bind("<Button-1>", lambda e: toggle_binds_expansion(latex_shortcuts_display_container, latex_shortcuts_label))

    # New LaTeX Shortcut Adder

    # LaTeX Shortcut Adder Container
    latex_shortcut_adder_container = tk.Frame(preferences_frame, bg=COLORS["bg_input"], name="latex_shortcut_adder_container")
    latex_shortcut_adder_container.pack()

    latex_shortcuts_adder_label = tk.Label(latex_shortcut_adder_container, bg=COLORS["bg_input"], font=FONTS["font_subtitle"], fg=COLORS["text_main"], text="Add a new LaTeX Shortcut ▼", name="latex_shortcuts_adder_label")
    latex_shortcuts_adder_label.pack()

    latex_shortcuts_adder_form_container = tk.Frame(latex_shortcut_adder_container, bg=COLORS["bg_input"], name="latex_shortcuts_adder_form_container")

    # Name Field Container
    latex_shortcut_adder_name_container = tk.Frame(latex_shortcuts_adder_form_container, bg=COLORS["bg_input"], name="latex_shortcut_adder_name_container")
    latex_shortcut_adder_name_container.pack()

    # Name Field Label
    latex_shortcut_adder_name_label = tk.Label(latex_shortcut_adder_name_container, bg=COLORS["bg_input"], font=FONTS["font_subtitle"], fg=COLORS["text_main"], text="LaTeX Shortcut Name: ", name="latex_shortcut_adder_name_label")
    latex_shortcut_adder_name_label.pack(side="left")

    # Name Field Entry
    latex_shortcut_adder_name_entry = tk.Entry(latex_shortcut_adder_name_container, name="latex_shortcut_adder_name_entry")
    latex_shortcut_adder_name_entry.pack(side="left")

    # Code Field Container
    latex_shortcut_adder_code_container = tk.Frame(latex_shortcuts_adder_form_container, bg=COLORS["bg_input"], name="latex_shortcut_adder_code_container")
    latex_shortcut_adder_code_container.pack()

    # Code Field Label
    latex_shortcut_adder_code_label = tk.Label(latex_shortcut_adder_code_container, bg=COLORS["bg_input"], font=FONTS["font_subtitle"], fg=COLORS["text_main"], text="LaTeX Shortcut Code: ", name="latex_shortcut_adder_code_label")
    latex_shortcut_adder_code_label.pack(side="left")

    # Code Field Entry
    latex_shortcut_adder_code_entry = tk.Text(latex_shortcut_adder_code_container, width=40, height=5, name="latex_shortcut_adder_code_entry")
    latex_shortcut_adder_code_entry.pack(side="left")

    # Error Message Display
    latex_shortcut_adder_error_msg = tk.Label(latex_shortcuts_adder_form_container, bg=COLORS["bg_input"], font=FONTS["font_subtitle"], fg="#FF0000", name="latex_shortcut_adder_error_msg")
    latex_shortcut_adder_error_msg.pack()

    # LaTeX New Shortcut Submit
    latex_shortcut_adder_submit = tk.Button(latex_shortcuts_adder_form_container, text="Add LaTeX Shortcut", bg=COLORS["border"], fg=COLORS["text_main"], bd=0, relief="flat", font=FONTS["font_subtitle"], command=(lambda COLORS=COLORS, FONTS=FONTS: add_latex_shortcut(latex_shortcut_adder_name_entry, latex_shortcut_adder_code_entry, latex_shortcut_adder_error_msg, latex_shortcuts_display_container, preferences_frame, COLORS, FONTS)), name="latex_shortcut_adder_submit")
    latex_shortcut_adder_submit.pack()
    
    latex_shortcuts_adder_label.bind("<Button-1>", lambda e: toggle_binds_expansion(latex_shortcuts_adder_form_container, latex_shortcuts_adder_label))

def destroy_preferences_setting(settings_subwindow_container):
    for widget in settings_subwindow_container.winfo_children():
        widget.destroy()