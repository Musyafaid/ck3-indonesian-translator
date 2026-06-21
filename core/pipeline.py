import os
import re

INPUT = "input_extracted"
OUTPUT = "output_mod"


# =========================
# AI TRANSLATOR (SIMULASI)
# =========================
def ai_translate(text):
    """
    GANTI INI NANTI DENGAN OPENAI / AI MODEL
    """
    return translate_basic_id(text)


# =========================
# TRANSLATION BASIC INDONESIA
# =========================
def translate_basic_id(text):
    replacements = {
        "You have no": "Kamu tidak memiliki",
        "has no": "tidak memiliki",
        "died": "meninggal",
        "from": "dari",
        "of": "karena",
        "Castle": "Benteng",
        "Temple": "Kuil",
        "City": "Kota",
        "Hall": "Aula",
        "Grand": "Megah",
        "ship": "kapal",
        "port": "pelabuhan",
        "docks": "dermaga"
    }

    result = text

    for k, v in replacements.items():
        result = re.sub(rf"\b{k}\b", v, result, flags=re.IGNORECASE)

    return result


# =========================
# SAFE CK3 PROTECTOR
# =========================
def safe_translate(text):

    # PROTECT:
    # $variable$
    # [chancellor|E]
    # [Function()]
    protected = re.findall(r"\$.*?\$|\[.*?\]", text)

    temp = text

    # replace semua CK3 system dengan placeholder
    for i, p in enumerate(protected):
        temp = temp.replace(p, f"__VAR{i}__")

    # translate only human text
    translated = ai_translate(temp)

    # restore CK3 system
    for i, p in enumerate(protected):
        translated = translated.replace(f"__VAR{i}__", p)

    return translated


# =========================
# CLEAN VALUE (CK3 FORMAT FIX)
# =========================
def clean_value(value):
    value = value.strip()

    # remove CK3 index :0 :1 :2
    value = re.sub(r"^[0-9]+\s+", "", value)

    # remove quotes
    if value.startswith('"') and value.endswith('"'):
        value = value[1:-1]

    return value


# =========================
# PROCESS FILE
# =========================
def process_file(in_path, out_path):

    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    with open(in_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []

    for line in lines:

        if ":" not in line:
            new_lines.append(line)
            continue

        try:
            key, value = line.split(":", 1)

            raw = clean_value(value)

            # SKIP EMPTY
            if not raw:
                new_lines.append(line)
                continue

            # SKIP PURE VARIABLE $...$
            if raw.startswith("$") and raw.endswith("$"):
                new_lines.append(line)
                continue

            # TRANSLATE
            translated = safe_translate(raw)

            # REBUILD CK3 LINE
            line = f'{key}: "{translated}"\n'

        except:
            pass

        new_lines.append(line)

    with open(out_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)


# =========================
# MAIN RUNNER
# =========================
def run():

    print("🚀 CK3 TRANSLATOR START (FINAL FIXED)")

    total = 0

    for root, _, files in os.walk(INPUT):
        for f in files:
            if f.endswith(".yml") or f.endswith(".txt"):
                in_path = os.path.join(root, f)
                out_path = in_path.replace(INPUT, OUTPUT)

                process_file(in_path, out_path)
                total += 1

    print(f"✅ DONE - {total} FILES TRANSLATED")


if __name__ == "__main__":
    run()
