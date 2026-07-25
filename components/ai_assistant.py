import tkinter as tk 
from tkinter import ttk 

from tkinter import filedialog 

import pyperclip 

import utils.ai_assist as ai_assist
import utils.shortcuts_unicode as shortcuts_unicode 
import utils.settings as settings 
import utils.auth as auth 
import utils.templates as templates 

#helper functions 

def _set_busy(status_label, button, busy, COLORS, compile_msg = "Thinking..."): 
    #if call made, disable compile button
    if busy: 
        button.config(state="disabled", text="...")
        status_label.config(text = compile_msg, fg=COLORS["text_muted"])

    else: 
        button.config(state="normal", text = "Generate")
        status_label.config(text = "", fg = COLORS["text_muted"])

def _compile_error(status_label, message, COLORS): 
    status_label.config(text=message, fg = "#FF0000")

def _display_text(parent, COLORS, FONTS, height = 8, name = None):
    widget = tk.Text(parent, height = height, bg = COLORS["bg_input"], fg = COLORS["text_main"], insertbackground = "white", bd =1, highlightbackground = COLORS["border"], 
highlightthickness =2, font = FONTS["font_subtitle"], padx = 12, pady = 12, wrap = "word", state ="disabled", name = name)
    
    return widget 

def _replace_text(widget, content): 
    widget.config(state="normal")
    widget.delete("1.0", "end")
    widget.insert("1.0", content)
    widget.config (state="disabled")

#function 1; for users to get syntax advice/LaTeX output by typing in English
def _build_latex_tab(parent, COLORS, FONTS): 
    latex_AI_tab = tk.Frame(parent, bg=COLORS["bg_main"], padx=15, pady =15, name ="LaTeX AI Tab" ) 
    tk.Label(latex_AI_tab, text="Describe the equation or structure required to get syntax/Ready-to-use LaTeX structures!",
    fg = COLORS["text_main"], bg = COLORS["bg_main"], font = FONTS["font_subtitle"])

    latex_AI_tab.pack(fill ="x", pady=(0,6)) 

    prompt_box = tk.Text(latex_AI_tab, height = 3,  fg = COLORS["text_main"], bg = COLORS["bg_main"], fonts = FONTS["font_subtitle"], insertbackground = "white", bd =1, highlightbackground = COLORS["border"], highlightthickness =1, padx = 12, pady = 10, wrap = "word", name = "latex_AI_display")
    prompt_box.pack(fill ="x")

    #frames to hold the status and control button side by side 
    controls = tk.Frame(latex_AI_tab, bg = COLORS["bg_main"])
    controls.pack(fill = "x", pady = (8,10))

    status = tk.Label(controls, text = "", fg = COLORS["text_muted"], bg = COLORS["bg_main"], font = FONTS["font_subtitle"], anchor ="w", name ="latex_ai_status")
    status.pack(side = "left", fill = "x", expand = True)

    generate_button = tk.Button(controls, text ="Generate", bg = COLORS["bg_main"], fg = COLORS["text_muted"], bd = 0, fonts = FONTS["font_subtitle"], name =" latex_ai_generate")
    generate_button.pack(side ="right")

    #actual output used
    output = _display_text(latex_AI_tab, COLORS, FONTS, height = 5, name = "latex_ai_output")
    output.pack(fill ="x")

    #AI explaination 
    explanation = _display_text(latex_AI_tab, COLORS, FONTS, height = 6, name ="latex_ai_explanation")
    explanation.pack(fill="both", expand = True, pady=(8,8))

    #for user's actions 
    actions = tk.Frame(latex_AI_tab, bg = COLORS["bg_main"])
    actions.pack(fill = "x")
    
    state ={"latex":""}

    def send_to_editor(): 
        if not state["latex"]:
            return 
        
        root = latex_AI_tab.winfo_toplevel()
        root.pending_latex_insert = state["latex"]
        pyperclip.copy(state["latex"])
        status.config(text ="Sent to LaTeX editor and copied to clipboard", fg = COLORS["action_green"])

    def copy_latex(): 
        if state["latex"]: 
            pyperclip.copy(state["latex"])
            status.config(text="copied to clipboard.", fg = COLORS["action_green"])

    tk.Button(actions, text="Copy", bg=COLORS["border"], fg=COLORS["text_main"], bd=0, font=FONTS["font_subtitle"], command=copy_latex,name="latex_copy_button").pack(side="right", padx=(6, 0))
    tk.Button(actions, text="Send to Editor", bg=COLORS["border"], fg=COLORS["text_main"], bd=0, font=FONTS["font_subtitle"], command=send_to_editor, name="latex_send_button").pack(side="right")

    def on_result(ok, payload): 
        _set_busy(status, generate_button, False, COLORS)
        if not ok: 
            _compile_error(status,payload, COLORS)
            return 
        
        state["latex"] = payload["latex"]
        _replace_text(output, payload["latex"])

        text = payload["explanation"]

        if payload.get("note"): 
            text += f"\n\nAssumption: {payload['note']}"
        _replace_text(explanation, text)
 
    def on_generate(event=None):
        description = prompt_box.get("1.0", "end-1c").strip()
        if not description: 
            _compile_error(status, "Describe what you want first.", COLORS)
            return "break"
        _set_busy(status, generate_button, True, COLORS)
        ai_assist.latex_from_description(latex_AI_tab, description, on_result)
        return "break"
 
    generate_button.config(command=on_generate)
    # Enter submits, Shift+Enter inserts a newline
    prompt_box.bind("<Return>", on_generate)
    prompt_box.bind("<Shift-Return>", lambda e: None)
 
    return latex_AI_tab

def build_ai_assistant(root, COLORS, FONTS): 
    outer = tk.Frame(root, bg = COLORS["bg_main"], padx = 20, pady =20, takefocus = True, name = "ai_assistant_frame")
    outer.pack(side ="top", fill ="both", expand = True)

    tk.Label(outer, text ="AI Assistant", fg = COLORS["text_main"], bg = COLORS["bg_main"], font = FONTS["font_subtitle"], name = "title_label").pack(fill ="x")

    tk.Label(outer, text ="Generate LaTeX from a description", fg = COLORS["text_muted"], bg = COLORS["bg_main"], font = FONTS["font_subtitle"], name ="subtitle_label").pack(fill ="x", pady = (0,15))

    notebook = ttk.Notebook(outer, name ="ai_notebook")
    notebook.pack(fill="both", expand = True)
    notebook.add(_build_latex_tab(notebook, COLORS, FONTS), text="LaTeX")

def destroy_ai_assistant(root): 
    for widget in root.winfo_children(): 
        if widget.winfo_name() != "navbar_frame": 
            widget.destroy()



