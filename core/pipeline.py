import json

def ai(text):
    return "ID: " + text


def load(p):
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def save(p, d):
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)


def run():
    memory = load("memory/translation_memory.json")
    glossary = load("memory/glossary.json")
    scan = load("memory/scan_rules.json")

    for text in scan["safe_texts"]:

        if text in glossary:
            memory[text] = glossary[text]
        elif text not in memory:
            memory[text] = ai(text)

    save("memory/translation_memory.json", memory)

    print("✅ TRANSLATION DONE")

if __name__ == "__main__":
    run()