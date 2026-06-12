import tkinter as tk 

import utils.shortcuts_unicode as shortcuts_unicode
import unicodedata 

def _unicode_name(ch): 
    try: 
        return unicodedata.name(ch)
    except (ValueError, TypeError): 
        return "Unnamed Character. Try Again"

#constantly updates bindings
def _update_bindings(container, COLORS, FONTS): 
    for child in container.winfo_children(): 
        child.destroy() 
    def refresh(): 
        _update_bindings(container, COLORS, FONTS)
    
    bindings = shortcuts_unicode.all_bindings()
    
    if not bindings: 
        empty = tk.Label(container, text="No shortcuts yet. Bind symbols from the search page", fg = COLORS["text_muted"], bg = COLORS["bg_main"], fonts= FONTS["font_subtitle"])
        empty.pack(fill="x", pady =10)
        return
    
    
def _binding_rows(bindings, binding_frame, COLORS, FONTS):
    for key, symbol in bindings.items():
        row = tk.Frame(binding_frame, bg=COLORS["bg_input"])
        row.pack(fill="x", pady=2)

        symbol_label = tk.Label(row, text=f"{symbol}  {unicode_search.get_unicode_name(symbol)}", bg=COLORS["bg_input"], fg=COLORS["text_main"], font=FONTS["font_subtitle"])
        symbol_label.pack(side="left", padx=(10,0))

        key_label = tk.Label(row, text=f"Bound to: '{key}'", bg=COLORS["bg_input"], fg=COLORS["text_muted"], font=FONTS["font_subtitle"])
        key_label.pack(side="left", padx=(10,0))

        binding.entry = tk.Button(row, text="Rebind", bg=COLORS["bg_button"], fg=COLORS["text_main"], font=FONTS["font_subtitle"], bd=0, padx=10, pady=5, command=lambda k=key, s=symbol: unicode_searchpanel._bind_key(binding_frame, s, unicode_search.get_unicode_name(s), COLORS, FONTS, lambda msg: key_label.config(text=f"Bound to: '{msg}'")))
        binding.entry.pack(side="right", padx=(0,10))
        
def build_unicode_setting_page(root, COLORS, FONTS):
    #frame that contains results frame 
    panel_frame =tk.Frame(root, bg= COLORS["bg_main"], padx=20, pady=20, takefocus=True, name ="unicode_shortcuts_settings")
    panel_frame.pack(side="top", fill="both", expand=True)

    #header 
    title_label = tk.Label(panel_frame, text="Unicode Shortcuts Settings", fg=COLORS["text_main"], bg=COLORS["bg_main"], font=FONTS["font_title"])
    title_label.pack(fill="x", pady=0)
    
    subtitle_label = tk.Label(panel_frame, text="Manage your unicode symbol shortcuts. Press Enter to Rebind", fg=COLORS["text_muted"], bg=COLORS["bg_main"], font=FONTS["font_subtitle"])
    subtitle_label.pack(fill="x", pady=(0, 15))

    #existing bindings frame
    binding_frame = tk.Frame(panel_frame, bg=COLORS["bg_main"])
    binding_frame.pack(fill="both", expand=True, pady=(15,0))  

    _update_bindings(binding_frames, COLORS, FONTS)

        
# Destroy function to tear down unicode shortcuts settings
def destroy_unicode_shortcuts_settings(root):

    # Remove all child widgets except for the navbar
    for widget in root.winfo_children():
        if widget.winfo_name() != "navbar_frame":
          widget.destroy()