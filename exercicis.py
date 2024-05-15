import json
import random


# https://freeling-user-manual.readthedocs.io/en/latest/tagsets/tagset-ca/#part-of-speech-verb
def read_json_file(filename):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: '{filename}' is not a valid JSON file.")
        return None


def read_verbs():
    with open("verbs.txt", "r") as _file:
        data = [
            _line.strip()
            for _line in _file.readlines()
            if _line.strip() and not _line.strip().startswith("#")
        ]

    return data


def get_word(form, persona):
    words = form[persona]
    for word in words:
        if word["variant"] not in ["4", "6", "7", "B", "V", "Z"]:
            w = word["word"]
            return w

    print(form)
    raise Exception("Not found")


MODES = 3
PERSONES = 6


def get_mode_tense():
    n = random.randint(0, MODES - 1)
    if n == 0:
        return "Indicatiu", "Present"
    if n == 1:
        return "Subjuntiu", "Present"
    if n == 2:
        return "Imperatiu", "Present"

    raise Exception("Number too big")


verbs = read_verbs()


def get_random_verb():
    n = random.randint(0, len(verbs) - 1)
    return verbs[n]


def get_verb_json(verb):
    subdir = verb[0:2]
    filename = f"data/jsons/{subdir}/{verb}.json"
    json_data = read_json_file(filename)
    return json_data


def get_random_code_pronom(mode):
    n = random.randint(0, 5)
    if mode == "Imperatiu":
        n = 1

    if n == 0:
        return "singular1", "jo"
    if n == 1:
        return "singular2", "tu"
    if n == 2:
        return "singular3", "ell, ella, vostè"

    if n == 3:
        return "plural1", "nosaltres"
    if n == 4:
        return "plural2", "vosaltres, vós"
    if n == 5:
        return "plural3", "ells, elles, vostès"

    raise Exception("Number too big")


def main():

    correct = 0
    DONE = 5
    entries = []
    for done in range(0, DONE):
        verb = get_random_verb()
        json_data = get_verb_json(verb)
        mode, tense = get_mode_tense()
        for form in json_data[verb]:
            if form.get("mode") == mode and form.get("tense") == tense:
                code, pronom = get_random_code_pronom(mode)
                forma = get_word(form, code)
                entry = f"{tense} {mode} {verb} {pronom} {forma}"
                print(f"\n--- {tense} - {mode} {verb} ({pronom})")
                answer = input().strip().lower()
                forma = [item.strip() for item in forma.split("/")]
                #                print(f"forma: {forma}, answer: {answer}")
                if answer in forma:
                    correct += 1
                    print("Correcte")
                    entries.append(entry)
                else:
                    forma_show = ", ".join(forma)
                    print(f"Resposta donada '{answer}', correcta '{forma_show}'")

                break

    print(f"Total: {DONE}, encerts: {correct}, errades: {DONE-correct}")
    with open('correct.txt', 'a') as _file:
        for entry in entries:
           _file.write(entry + "\n")

if __name__ == "__main__":
    comb = len(verbs) * MODES * PERSONES
    print(f"Combinacions: {comb}")
    main()
