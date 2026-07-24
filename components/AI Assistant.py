import tkinter as tk 
from tkinter import ttk 

from tkinter import fieldialog 

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
    status_label.config(text=message, fg = COLORS["#FF0000"])

def _display_text(parent, COLORS, FONTS, height = 8, name = None):
    widget = tk.Text(parent, height = height, bg = COLORS["bg_input"], fg = COLORS["text_main"], insertbackground = "white", bd =1, highlightbackground = COLORS["border"], 
highlightthickness =2, font = FONTS["font_subtitle"], padx = 12, pady = 12, wrap = "word", state ="disabled", name = name)
    
    return widget 

def _replace_text(widget, content): 
    widget.config(state="normal")
    widget.delete("1.0", "end")
    widget.insert("1", content)
    widget.config (state="disabled")

#function 1; for users to get syntax advice/LaTeX output by typing in English
def _build_latex_tab(parent, COLORS, FONTS): 
    latex_AI_tab = tk.Frame(parent, bg=COLORS["bg_main"], padx=15, pady =15, name ="LaTeX AI Tab" ) 
    tk.Label(latex_AI_tab, text="Describe the equation or structure required to get syntax/Ready-to-use LaTeX structures!",
    fg = COLORS["text_main"], bg = COLORS["bg_main"], fonts = FONTS["font_subtitle"])

    latex_AI_tab.pack(fill ="x", pady=(0,6)) 

    prompt_box = tk.Text(latex_AI_tab, height = 3,  fg = COLORS["text_main"], bg = COLORS["bg_main"], fonts = FONTS["font_subtitle"]
                         insertbackground = "white", bd =1, highlightbackground = COLORS["border"], highlightthickness =1, padx = 12, pady = 10, 
                         wrap = "word", name = "latex_AI_display")
    prompt_box.pack(fill ="x")

    #frames to hold the status and control button side by side 
    controls = tk.Frame(latex_AI_tab, bg = COLORS["bg_main"])
    controls.pack(fill = "x", pady = (8,10))

    status = tk.Frame(latex_AI_tab, bg = COLORS["bg_main"], fg = COLORS["text_muted"], fonts = FONTS["font_subtitle"], name = "latex_ai_status")
    status.pack(side = "left", fill = "x", expand = True)

    generate_button = tk.Button(controls, text ="Generate", bg = COLORS["bg_main"], fg = COLORS["text_muted"], bd = 0, fonts = FONTS["font_subtitle"], name =" latex_ai_generate")
    generate_button.pack(side ="right")

    #actual output used
    output = _display_text(latex_AI_tab, COLORS, FONTS, height = 5, name = "latex_ai_output")
    output.pack(fill ="x")

    #AI explaination 
    explaination = _display_text(latex_AI_tab, COLORS, FONTS, height = 6, bane ="latex_ai_explaination")
    explaination.pack(fill="both", expand = True, pady=(8,8))

    #for user's actions 
    actions = tk.Frame(latex_AI_tab, bg = COLORS["bg_main"])
    actions.pack(fill = "x")

state ={"latex":""}

