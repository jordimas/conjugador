import json
import random

#https://freeling-user-manual.readthedocs.io/en/latest/tagsets/tagset-ca/#part-of-speech-verb
def read_json_file(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: '{filename}' is not a valid JSON file.")
        return None

def read_verbs():
    with open("verbs.txt", 'r') as _file:
        data = [_line.strip() for _line in _file.readlines() if _line.strip() and not _line.strip().startswith('#')]
        
    return data
        
def get_word(form, persona):
    words = form[persona]
    for word in words:
        if word["variant"] not in ["4", "6", "7", "B", "V", "Z"]:
            w = word["word"]
            return w

    print(form)    
    raise Exception("Not found")
    
def get_mode_tense():
    n = random.randint(0, 1)
    if n == 0:
        return "Indicatiu", "Present"
    if n == 1:
        return "Subjuntiu", "Present"
            
    raise Exception("Number too big")            
            
            
def main():
    verbs = read_verbs()
 
    for verb in verbs:
        subdir = verb[0:2]
        filename = f"data/jsons/{subdir}/{verb}.json"
        json_data = read_json_file(filename)
        mode, tense = get_mode_tense()
        for form in json_data[verb]:
            if form.get("mode") == mode and form.get("tense") == tense:
                forma = get_word(form, "singular1")
                print(f"--- {tense} - {mode} {verb} - {forma}")
                break
                
if __name__ == "__main__":
    main()            
