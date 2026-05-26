#search function for unicode 

import unicodedata
from unittest import result 

# check if the query is valid and not empty
#check the unicode data in the range of common used symbols

def search_by_name(query, limit=50):
    if not query or not query.strip(): return [] 
    query = query.strip().upper() 
    results = []
    for codepoint in range(0x20, 0x2FFF): 
        ch = chr(codepoint)
        name = unicodedata.name(ch, "")
        if name and q in name: 
            results.append((ch, name, codepoint))
            if len(results) >= limit:
                break 
            
    return results

def search_by_codepoint(text):
    #if user input decimals
    try: 
        cleaned = text.strip().upper()
        if cleaned.startswith('#'): 
            cp = int(cleaned[1:], 16)
    #if user input 'U+2FFF' or '2FFF' or decimals
        else: 
            cleaned = cleaned.removeprefix('U+').removeprefix('0X')
            cp = int(cleaned, 16)
        ch = chr(cp) 
        name = unicodedata.name(ch, "UNNAMED CHARACTER") 
        return (ch, name, cp)
    #not a valid unicode codepoint or out of range
    except (ValueError, OverflowError):
        return None 
    
#search by codepoint followed by name if cp fails 
def search(query, limit=50):
    by_codepoint = search_by_codepoint(query)
    if by_codepoint: 
        return[by_codepoint]
    return search_by_name(query, limit)