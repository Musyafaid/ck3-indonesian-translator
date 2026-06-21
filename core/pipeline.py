import os
import re
import json

INPUT = "input_extracted"
OUTPUT = "output_mod"


# =========================
# TRANSLATOR (SIMULASI / GANTI AI)
# =========================
def ai_translate(text):
    # nanti bisa diganti OpenAI
    return translate_id(text)


# =========================
# SIMPLE INDONESIAN TRANSLATION
# =========================
def translate_id(text):
    replacements = {
        "died": "meninggal",
        "from": "dari",
        "of": "karena",
        "War": "Perang",
        "Castle": "Benteng",
        "Temple": "Kuil",
        "City": "Kota",
        "port": "pelabuhan",
        "ship": "kapal",
        "repair": "memperbaiki"
    }

    result = text
    for k, v in replacements.items():
        result = re.sub(rf"\b{k}\b", v, result, flags=re.IGNORECASE)

    return result


# =========================
# SAFE CK3 PROTECTION
# =========================
def safe_translate(text):
    # protect CK3 variables $...$
    protected = re.findall(r"\$.*?\$", text)

    temp = text

    for i, p in enumerate(protected):
        temp = temp.replace(p, f"__VAR{i}__")

    translated = ai_translate(temp)

    for i, p in enumerate(protected):
        translated = translated.replace(f"__VAR{i}__", p)

    return translated


# =========================
# CLEAN CK3 VALUE
# =========================
def clean_value(value):
    value = value.strip()

    # remove CK3 numeric prefix (:0 :1 :2)
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

        # skip empty / invalid
        if ":" not in line:
            new_lines.append(line)
            continue

        try:
            key, value = line.split(":", 1)

            raw = clean_value(value)

            # =========================
            # SKIP CK3 VARIABLE TOTAL
            # =========================
            if raw.startswith("$") and raw.endswith("$"):
                new_lines.append(line)
                continue

            # skip empty
            if not raw:
                new_lines.append(line)
                continue

            # translate
            translated = safe_translate(raw)

            # rebuild CK3 format (KEEP KEY + INDEX)
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
    print("🚀 CK3 TRANSLATOR START (FIXED VERSION)")

    total = 0

    for root, _, files in os.walk(INPUT):
        for f in files:
            if f.endswith(".yml"):
                in_path = os.path.join(root, f)
                out_path = in_path.replace(INPUT, OUTPUT)

                process_file(in_path, out_path)
                total += 1

    print(f"✅ DONE - {total} FILES")


if __name__ == "__main__":
    run()
