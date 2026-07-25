import json 

import utils.gemini_api as gemini

#to make it a dict
def _parse(ok, result, keys): 
    if not ok: 
        return False, result 
    try: 
        data = json.loads(result)
    except json.JSONDecodeError:
        return False, "Gemini returned malformed JSON"
    
    #checks through field of AI responses for what we want
    for k in keys: 
        if k not in data:
            return False, f"Gemini response was missing the '{k}' field."
        
    return True, data

#feature 1, LaTeX generate from plain English 

LATEX_SYSTEM = """You are a LaTeX expert embedded in an equation Editor. 
The user will describe a mathematical expression or structure in plain Language. Return the LaTeX that produces it. 

Constraints: 
1) Only output the math body only. No $ delimiters, no \\begin{document}, no \\documentclass, no markdown code fences. 
2) If the description is ambiguous, pick the most standard reading and say that you assumed in the "note" field. 
3) Keep it to a single expression unless user asked for several. 
4) "Explanation" field should describe what each non-obvious command does so that users can learn the syntax. """
    

LATEX_SCHEMA ={ 
    "type": "object", 
    "properties":{
        "latex":{
            "type":"string",
            "description": "The LaTeX code, math body only, no delimiters.",
        }, 
        "explanation":{
            "type":"string",
            "description": "Short plain language breakdown of commmands used."
        },
        "note":{
            "type":"string", 
            "description": "Any assumption made about an ambiguous request. Empty string if none."
        }, 
    },
    "required": ["latex", "explanation", "note"]
}

def latex_from_description(widget, description, on_done): 
    def handle (ok,result): 
        on_done(*_parse(ok,result,["latex", "explanation", "note"]))   
    print(">>> calling generate_async now")
    gemini.generate_async(
        widget,
        prompt =f"Produce LaTeX for:{description}", 
        on_done = handle, 
        system_instruction = LATEX_SYSTEM, 
        schema = LATEX_SCHEMA, 
        temperature = 0.1, #force AI for conventional answer
        )    