import json
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
        if word["variant"] in ["C", "0"]:
            w = word["word"]
            return w

    print(form)    
    raise Exception("Not found")

verbs = read_verbs()
 
for verb in verbs:
    # Example usage:
    subdir = verb[0:2]
    filename = f"data/jsons/{subdir}/{verb}.json"
    json_data = read_json_file(filename)
    for form in json_data[verb]:
        if form.get("mode") == "Indicatiu" and form.get("tense") == "Present":
            verb = get_word(form, "singular1")
            print(f"--- {verb}")            
            print(verb)
            break
