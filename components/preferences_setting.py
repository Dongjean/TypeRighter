import tkinter as tk
from tkinter import ttk

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

    # Display the Current Keybinds Under the Selected Template
    
    # Current Keybinds Container
    curr_keybinds_container = tk.Frame(preferences_frame, bg=COLORS["bg_input"], name="curr_keybinds_container")
    curr_keybinds_container.pack()
    
    # Keybinds Label
    curr_keybinds_label = tk.Label(curr_keybinds_container, bg=COLORS["bg_input"], font=FONTS["font_subtitle"], fg=COLORS["text_main"], text="Current Keybinds", name="curr_keybinds_label")
    curr_keybinds_label.pack()

    # Fake list of keybinds
    curr_keybinds = {
        "\\": "Breakout",
        "a": "Close",
        "`": "Exit",
        "q": "⊂",
        "w": "∅",
        "e": "∈",
        "r": "⊂",
        "t": "⊆",
    }

    # Show Each Keybind
    for key, bind in curr_keybinds.items():
        
        # This Keybind's Container
        keybind_container = tk.Frame(curr_keybinds_container, bg=COLORS["bg_input"], name=f"{key}_keybind_container")
        keybind_container.pack(pady=2, anchor="w")

        # The Key Label
        key_label = tk.Label(keybind_container, bg=COLORS["bg_input"], font=FONTS["font_subtitle"], highlightbackground="white", highlightthickness=1, fg=COLORS["text_main"], text=key, name=f"{key}_key_label")
        key_label.pack(side="left")

        # The Corresponding Bind Label
        bind_label = tk.Label(keybind_container, bg=COLORS["bg_input"], font=FONTS["font_subtitle"], fg=COLORS["text_main"], text=bind, name=f"{key}_bind_label")
        bind_label.pack(side="left")

        # This Keybind's Unbinder
        keybind_unbinder =tk.Button(keybind_container, text="Unbind", fg=COLORS["action_green"], bg=COLORS["bg_input"], font=FONTS["font_subtitle"], bd=0, command=None, name=f"{key}_keybind_unbinder")
        keybind_unbinder.pack(side="right", padx=8)
    
    # Current Phrase Bindings Container
    curr_phrasebinds_container = tk.Frame(preferences_frame, bg=COLORS["bg_input"], name="curr_phrasebinds_container")
    curr_phrasebinds_container.pack()

    # Phrase Bindings Label
    curr_phrasebinds_label = tk.Label(curr_phrasebinds_container, bg=COLORS["bg_input"], font=FONTS["font_subtitle"], fg=COLORS["text_main"], text="Current Phrase Bindings", name="curr_phrasebinds_label")
    curr_phrasebinds_label.pack()

    # Fake list of Phrase Bindings
    curr_phrasebinds = {
        "alpha": "α",
    }

    # Show Each Phrase Binding
    for phrase, bind in curr_phrasebinds.items():
        
        # This Phrase Binding's Container
        phrasebind_container = tk.Frame(curr_phrasebinds_container, bg=COLORS["bg_input"], name=f"{phrase}_phrasebind_container")
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

def destroy_preferences_setting(settings_subwindow_container):
    for widget in settings_subwindow_container.winfo_children():
        widget.destroy()