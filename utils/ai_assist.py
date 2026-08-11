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


#Feature 2 Contextual Guidance -> Explain Notation, suggest Unicode Characters 
NOTATION_SYSTEM = """You help users of a symbol-typing tool understand and find mathematical, scientific, and technical notation. 
The User gives you either a symbol they can't recognise, or a description of a concept they want a symbol for. 
    
For each suggested symbol return: 
- the character itself 
- its official Unicode Name (e.g. N-ARY SUMMATION)
- its codepoint as a bare uppercase hex string with prefix (U+2211)
- the LaTeX command that produces it, if one exists (else empty string)
- what it means and the fields it's used in
    
Constraints: 
1) Only suggest characters that exist in Unicode. Never invent a codepoint. If unsure the exact codepoint, omit 
the symbol entirely. 
2) Return between 1 to 6 symbols, most relevant first
3) If the user pasted a symbol, the first entry must be that exact symbol. 
4) Watch for lookalikes and mention them: the meaning of  ∈ vs ϵ vs ε, or ∏ vs Π, matters and users confuse them constantly"""


NOTATION_SCHEMA = {
    "type": "object",
    "properties": {
        "summary": {
            "type": "string",
            "description": "One or two sentences answering the user's question directly.",
        },
        "symbols": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "character": {"type": "string"},
                    "unicode_name": {"type": "string"},
                    "codepoint_hex": {
                        "type": "string",
                        "description": "Uppercase hex with 'U+' prefix",
                    },
                    "latex": {"type": "string"},
                    "meaning": {"type": "string"},
                },
                "required": ["character", "unicode_name", "codepoint_hex", "latex", "meaning"],
            },
        },
    },
    "required": ["summary", "symbols"],
}

def explain_notation(widget, query, on_done):
    def handle(ok, result):
        ok2, data = _parse(ok, result, ["summary", "symbols"])
        if ok2:
            data["symbols"] = verify_symbols(data.get("symbols", []))
        on_done(ok2, data)
 
    gemini.generate_async(
        widget,
        prompt=query,
        on_done=handle,
        system_instruction=NOTATION_SYSTEM,
        schema=NOTATION_SCHEMA,
        temperature=0.1,
    )
 
 #double check with database of unicode
def verify_symbols(symbols):
    import unicodedata
 
    verified = []
    for s in symbols:
        char = s.get("character", "")
        if not char:
            continue
        try:
            cp = ord(char[0])
        except TypeError:
            continue
 
        name = unicodedata.name(chr(cp), "")
        if not name:
            continue  

        verified.append({
            "character": chr(cp),
            "unicode_name": name,          # from unicodedata, not the model
            "codepoint": cp,               
            "latex": s.get("latex", ""),
            "meaning": s.get("meaning", ""),
        })
 
    return verified