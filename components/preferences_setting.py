import tkinter as tk
from tkinter import ttk

import utils.shortcuts_unicode as shortcuts_unicode

def build_preferences_setting(settings_subwindow_container, COLORS, FONTS):
    
    # Preferences Frame
    preferences_frame = tk.Frame(settings_subwindow_container, bg=COLORS["bg_input"], takefocus=True, name="preferences_frame")
    preferences_frame.pack(expand=True)

    # Templates Selector Container
    template_selector_container = tk.Frame(preferences_frame, bg=COLORS["bg_input"], name="template_selector_container")
    template_selector_container.pack(fill="x", anchor="center")

    # Templates Selector Label
    template_selector_label = tk.Label(template_selector_container, bg=COLORS["bg_input"], font=FONTS["font_subtitle"], fg=COLORS["text_main"], text="Selected Template", name="template_selector_label")
    template_selector_label.pack()
    
    # Fake list of templates
    curr_templates = ["default", "CS1231", "MA1508E"]
    # Template Selector Dropdown Menu
    template_selector = ttk.Combobox(template_selector_container, values=curr_templates, state="readonly")
    template_selector.set(curr_templates[0])
    template_selector.pack()

    # Display the Keybinds Under the Selected Template
    
    # Current Keybinds Container
    keybinds_container = tk.Frame(preferences_frame, bg=COLORS["bg_input"], name="curr_keybinds_container")
    keybinds_container.pack()
    
    # Keybinds Label
    keybinds_label = tk.Label(keybinds_container, bg=COLORS["bg_input"], font=FONTS["font_subtitle"], fg=COLORS["text_main"], text="Current Keybinds", name="keybinds_label")
    keybinds_label.pack()

    def toggle_widget_visibility(widget):
        
        # If the widget is already visible, turn it off
        if widget.winfo_ismapped():
            widget.pack_forget()
        else:
            widget.pack()
            
    keybinds_display_container = tk.Frame(keybinds_container, bg=COLORS["bg_input"], name="phrasebinds_display_container")
    
    # Get the Dictionary of Keybinds
    curr_keybinds = shortcuts_unicode.all_bindings()

    # Show Each Keybind
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
            keybind_unbinder = tk.Button(keybind_container, text="Unbind", fg=COLORS["action_green"], bg=COLORS["bg_input"], font=FONTS["font_subtitle"], bd=0, command=lambda key=key: shortcuts_unicode.remove_binding(key), name=f"{key}_keybind_unbinder")
            keybind_unbinder.pack(side="right", padx=8)
    
    keybinds_label.bind("<Button-1>", lambda e: toggle_widget_visibility(keybinds_display_container))

    # Current Phrase Bindings Container
    phrasebinds_container = tk.Frame(preferences_frame, bg=COLORS["bg_input"], name="phrasebinds_container")
    phrasebinds_container.pack()

    # Phrase Bindings Label
    phrasebinds_label = tk.Label(phrasebinds_container, bg=COLORS["bg_input"], font=FONTS["font_subtitle"], fg=COLORS["text_main"], text="Current Phrase Bindings", name="phrasebinds_label")
    phrasebinds_label.pack()

    # Fake list of Phrase Bindings
    curr_phrasebinds = {
        "alpha": "α",
    }

    phrasebinds_display_container = tk.Frame(phrasebinds_container, bg=COLORS["bg_input"], name="phrasebinds_display_container")

    # Show Each Phrase Binding
    for phrase, bind in curr_phrasebinds.items():
        
        # This Phrase Binding's Container
        phrasebind_container = tk.Frame(phrasebinds_display_container, bg=COLORS["bg_input"], name=f"{phrase}_phrasebind_container")
        phrasebind_container.pack()

        # The Phrase Label
        phrase_label = tk.Label(phrasebind_container, bg=COLORS["bg_input"], font=FONTS["font_subtitle"], highlightbackground="white", highlightthickness=1, fg=COLORS["text_main"], text=phrase, name=f"{phrase}_phrase_label")
        phrase_label.pack(side="left")

        # The Corresponding Bind Label
        bind_label = tk.Label(phrasebind_container, bg=COLORS["bg_input"], font=FONTS["font_subtitle"], fg=COLORS["text_main"], text=bind, name=f"{phrase}_bind_label")
        bind_label.pack(side="left")

        # This Phrase Binding's Unbinder
        phrasebind_unbinder =tk.Button(phrasebind_container, text="Unbind", fg=COLORS["action_green"], bg=COLORS["bg_input"], font=FONTS["font_subtitle"], bd=0, command=None, name=f"{phrase}_phrasebind_unbinder")
        phrasebind_unbinder.pack(side="right", padx=8)
    
    phrasebinds_label.bind("<Button-1>", lambda e: toggle_widget_visibility(phrasebinds_display_container))

def destroy_preferences_setting(settings_subwindow_container):
    for widget in settings_subwindow_container.winfo_children():
        widget.destroy()