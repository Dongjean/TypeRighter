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
    latex_AI_tab = tk.Frame(parent, bg=COLORS["bg_main"], padx=15, pady =15, name ="latex_ai_tab" ) 
    latex_AI_tab.pack(fill ="both", expand = True)

    tk.Label(latex_AI_tab, text="Describe the equation or structure required to get syntax/Ready-to-use LaTeX structures!",
    fg = COLORS["text_main"], bg = COLORS["bg_main"], font = FONTS["font_subtitle"], anchor ="w").pack(fill ="x", pady=(0,6)) 

    prompt_box = tk.Text(latex_AI_tab, height = 3,  fg = COLORS["text_main"], bg = COLORS["bg_main"], font = FONTS["font_subtitle"], insertbackground = "white", bd =1, highlightbackground = COLORS["border"], highlightthickness =1, padx = 12, pady = 10, wrap = "word", name = "latex_ai_display")
    prompt_box.pack(fill ="x")

    #frames to hold the status and control button side by side 
    controls = tk.Frame(latex_AI_tab, bg = COLORS["bg_main"])
    controls.pack(fill = "x", pady = (8,10))

    status = tk.Label(controls, text = "", fg = COLORS["text_muted"], bg = COLORS["bg_main"], font = FONTS["font_subtitle"], anchor ="w", name="latex_ai_status")
    status.pack(side = "left", fill = "x", expand = True)

    generate_button = tk.Button(controls, text ="Generate", bg = COLORS["border"], fg = COLORS["text_main"], bd = 0, font = FONTS["font_subtitle"], name=" latex_ai_generate")
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

def _build_notation_tab(parent, COLORS, FONTS):
    frame = tk.Frame(parent, bg=COLORS["bg_main"], padx=15, pady=15, name="notation_ai_tab")
 
    tk.Label(
        frame,
        text="Paste a symbol you don't recognise, or describe one you're looking for:",
        fg=COLORS["text_main"], bg=COLORS["bg_main"], font=FONTS["font_subtitle"], anchor="w",
    ).pack(fill="x", pady=(0, 6))
 
    query = tk.StringVar()
    entry = tk.Entry(frame, textvariable=query, bg=COLORS["bg_input"], fg=COLORS["text_main"],
                     insertbackground="white", bd=1, highlightbackground=COLORS["border"],
                     highlightthickness=1, font=FONTS["font_subtitle"], name="notation_entry")
    entry.pack(fill="x", ipady=6)
 
    controls = tk.Frame(frame, bg=COLORS["bg_main"])
    controls.pack(fill="x", pady=(8, 10))
 
    status = tk.Label(controls, text="", fg=COLORS["text_muted"], bg=COLORS["bg_main"],
                      font=FONTS["font_subtitle"], anchor="w", name="notation_status")
    status.pack(side="left", fill="x", expand=True)
 
    generate_btn = tk.Button(controls, text="Generate", bg=COLORS["border"],
                             fg=COLORS["text_main"], bd=0, relief="flat",
                             font=FONTS["font_subtitle"], name="notation_ask_button")
    generate_btn.pack(side="right")
 
    summary = _display_text(frame, COLORS, FONTS, height=4, name="notation_summary")
    summary.pack(fill="x")
 
    results_frame = tk.Frame(frame, bg=COLORS["bg_main"], name="notation_results")
    results_frame.pack(fill="both", expand=True, pady=(10, 0))
 
    def bind_symbol(char, name):
        """
        Reuse your existing binding flow. This deliberately calls the same
        shortcuts_unicode / templates functions the Unicode Search panel uses,
        so an AI-suggested symbol is bound exactly like a hand-searched one --
        no second code path to keep in sync.
        """
        import components.unicode_searchpanel as unicode_searchpanel
        root = frame.winfo_toplevel()
        unicode_searchpanel._bind_key(
            root, char, name, COLORS, FONTS,
            lambda msg: status.config(text=msg, fg=COLORS["accent_blue"]),
        )
 
    def render(symbols):
        for child in results_frame.winfo_children():
            child.destroy()
 
        for s in symbols:
            row = tk.Frame(results_frame, bg=COLORS["bg_input"])
            row.pack(fill="x", pady=2)
 
            tk.Label(row, text=s["character"], fg=COLORS["text_main"], bg=COLORS["bg_input"],
                     font=FONTS["font_title"], width=3).pack(side="left", padx=(8, 4))
 
            info = tk.Frame(row, bg=COLORS["bg_input"])
            info.pack(side="left", fill="x", expand=True)
 
            header = f"{s['unicode_name']} (U+{s['codepoint']:04X})"
            if s.get("latex"):
                header += f"   {s['latex']}"
            tk.Label(info, text=header, fg=COLORS["text_muted"], bg=COLORS["bg_input"],
                     font=FONTS["font_subtitle"], anchor="w").pack(fill="x")
            tk.Label(info, text=s.get("meaning", ""), fg=COLORS["text_main"],
                     bg=COLORS["bg_input"], font=FONTS["font_subtitle"], anchor="w",
                     wraplength=420, justify="left").pack(fill="x")
 
            btn = tk.Button(row, text="bind", fg=COLORS["action_green"], bg=COLORS["bg_input"],
                            font=FONTS["font_subtitle"], bd=0)
            btn.config(command=lambda c=s["character"], n=s["unicode_name"]: bind_symbol(c, n))
            btn.pack(side="right", padx=8)
 
    def on_result(ok, payload):
        _set_busy(status, generate_btn, False, COLORS)
        if not ok:
            _compile_error(status, payload, COLORS)
            return
        _replace_text(summary, payload["summary"])
        render(payload["symbols"])
        if not payload["symbols"]:
            status.config(text="No verifiable symbols found.", fg=COLORS["text_muted"])
 
    def on_ask(event=None):
        q = query.get().strip()
        if not q:
            _compile_error(status, "Enter a symbol or a description first.", COLORS)
            return "break"
        _set_busy(status, generate_btn, True, COLORS)
        ai_assist.explain_notation(frame, q, on_result)
        return "break"
 
    generate_btn.config(command=on_ask)
    entry.bind("<Return>", on_ask)
    entry.focus_set()
 
    return frame

def build_ai_assistant(root, COLORS, FONTS): 
    outer = tk.Frame(root, bg = COLORS["bg_main"], padx = 20, pady =20, takefocus = True, name = "ai_assistant_frame")
    outer.pack(side ="top", fill ="both", expand = True)

    tk.Label(outer, text ="AI Assistant", fg = COLORS["text_main"], bg = COLORS["bg_main"], font = FONTS["font_subtitle"], name = "title_label").pack(fill ="x")

    tk.Label(outer, text ="Generate LaTeX and look up notation", fg = COLORS["text_muted"], bg = COLORS["bg_main"], font = FONTS["font_subtitle"], name ="subtitle_label").pack(fill ="x", pady = (0,15))

    notebook = ttk.Notebook(outer, name ="ai_notebook")
    notebook.pack(fill="both", expand = True)
    notebook.add(_build_latex_tab(notebook, COLORS, FONTS), text="LaTeX")
    notebook.add(_build_notation_tab(notebook, COLORS, FONTS), text="Notation")

def destroy_ai_assistant(root): 
    for widget in root.winfo_children(): 
        if widget.winfo_name() != "navbar_frame": 
            widget.destroy()



