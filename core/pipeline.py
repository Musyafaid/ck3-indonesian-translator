import os
import json
import re

INPUT = "input_extracted"
OUTPUT = "output_mod"


# =========================
# AI TRANSLATOR (SIMULASI)
# =========================
def ai_translate(text):
    # NANTI BISA DIGANTI OPENAI API
    return "ID: " + text


# =========================
# SAFE TRANSLATE (CK3 PROTECTION)
# =========================
def safe_translate(text):
    # ambil semua CK3 script seperti [GetTrait(...)]
    protected = re.findall(r"\[.*?\]", text)

    temp = text

    # ganti jadi placeholder
    for i, p in enumerate(protected):
        temp = temp.replace(p, f"__VAR{i}__")

    # translate teks biasa
    translated = ai_translate(temp)

    # restore CK3 script
    for i, p in enumerate(protected):
        translated = translated.replace(f"__VAR{i}__", p)

    return translated


# =========================
# LOAD & SAVE JSON
# =========================
def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# =========================
# PROCESS FILE (MIRROR MODE)
# =========================
def process_file(in_path, out_path, memory, glossary):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    with open(in_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []

    for line in lines:
        original_line = line

        if ":" in line:
            try:
                key, value = line.split(":", 1)

                text = value.strip().strip('"')

                # skip empty
                if not text:
                    new_lines.append(line)
                    continue

                # glossary check
                if text in glossary:
                    translated = glossary[text]

                # memory check
                elif text in memory:
                    translated = memory[text]

                # AI translate
                else:
                    translated = safe_translate(text)
                    memory[text] = translated

                # replace value
                line = f"{key}: \"{translated}\"\n"

            except:
                pass

        new_lines.append(line)

    with open(out_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)


# =========================
# MAIN PIPELINE
# =========================
def run():
    print("🚀 START TRANSLATION PIPELINE")

    memory = load_json("memory/translation_memory.json")
    glossary = load_json("memory/glossary.json")

    total_files = 0

    for root, _, files in os.walk(INPUT):
        for f in files:
            if f.endswith(".yml"):
                in_path = os.path.join(root, f)

                # mirror path ke output_mod
                out_path = in_path.replace(INPUT, OUTPUT)

                process_file(in_path, out_path, memory, glossary)

                total_files += 1

    save_json("memory/translation_memory.json", memory)

    print(f"✅ DONE - {total_files} FILES TRANSLATED")


if __name__ == "__main__":
    run()
