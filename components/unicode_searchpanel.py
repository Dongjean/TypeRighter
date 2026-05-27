import tkiner as tk 
import utils.unicode_search as unicode_search 

def _do_search(query, results_frame, COLORS, FONTS): 

    #remove all rows currently shown in the results frame
    for child in results_frame.winfo_children(): 
        child.destroy()

    # using the search function to get the results for the query
    results = unicode_search.search(query.get())

    # if there are no results, then inform users to check the unicode codepoint
    if not results: 
        empty = tk.Label(results_frame, text="No relevant symbols found. Check unicode codepoint", fg = COLORS["text_muted"], bg=COLORS["bg_main"],font=FONTS["font_subtitles"])
        empty.pack(fill="x", pady=10) 
        return 
    
    #for each valid input, display results in results frames as rows 

    for ch, name, cp in results: 
        row = tk.Frame(results_frame, bg=COLORS["bg_input"])
        row.pack(fill="x",pady=2) 

        symbol_icon = tk.Label(row, text=ch, fg=COLORS["text_main"], bg=COLORS["bg_input"],font=FONTS["font_title"])
        symbol_icon.pack(side="left",padx=(8,4))

        symbol_info = tk.Label(row, text=f"{name} (U+{cp:04X})", fg=COLORS["text_muted"], bg=COLORS["bg_input"],font=FONTS["font_subtitle"], anchor="w")
        symbol_info.pack(side="left", fill='x', expand = True) 

def build_unicode_search_panel(root, COLORS, FONTS):

    #frame for the panel that contains results frame 

    panel_frame =tk.Frame(root, bg= COLORS["bg_main"], padx=20, pady=20, takefocus=True, name ="unicode_search_panel")
    panel_frame.pack(side="top", fill="both", expand=True)

    #header 
    title_label = tk.Label(panel_frame, text="Unicode Symbol Search", fg=COLORS["text_main"], bg=COLORS["bg_main"], font=FONTS["font_title"])
    title_label.pack(fill="x", pady=0)
    
    subtitle_label = tk.Label(panel_frame, text="Search for unicode symbols by name or codepoint", fg=COLORS["text_muted"], bg=COLORS["bg_main"], font=FONTS["font_subtitle"])
    subtitle_label.pack(fill="x", pady=(0, 15))

    #search box, query is a variable that holds the string that user inputs in search bar

    query = tk.StringVar()
    search_box = tk.Entry(panel_frame, textvariable=query, bg=COLORS["bg_input"], fg=COLORS["text_main"], insertbackground="white", bd=1, highlightbackground=COLORS["border"], highlightthickness=1, font=FONTS["font_subtitle"])
    search_box.pack(fill="x", ipady = 6)

    #results frame that holds the search results
    results_frame = tk.Frame(panel_frame, bg=COLORS["bg_main"])
    results_frame.pack(fill="both", expand=True, pady=(15,0))  

    #put the cursor in the search box the moment the panel is built
    search_box.focus_set()

    #listen to changes in the search box and do search whenever there is a change
    query.trace("w", lambda name, index, mode: _do_search(query, results_frame, COLORS, FONTS))

# Destroy function to tear down unicode search panel
def destroy_unicode_search_panel(root):

    # Remove all child widgets except for the navbar
    for widget in root.winfo_children():
        if widget.winfo_name() != "navbar_frame":
          widget.destroy()