import os
import json

BLACKLIST = ["[", "]", "$", "%", "#"]

def safe(text):
    if not text:
        return False
    return not any(b in text for b in BLACKLIST)


def scan():
    result = {"safe_texts": [], "blacklist": []}

    for root, _, files in os.walk("input_extracted"):
        for f in files:
            if f.endswith(".yml"):
                path = os.path.join(root, f)

                with open(path, "r", encoding="utf-8") as file:
                    for line in file:
                        if ":" in line:
                            text = line.split(":", 1)[1].strip().strip('"')

                            if safe(text):
                                result["safe_texts"].append(text)
                            else:
                                result["blacklist"].append(text)

    with open("memory/scan_rules.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print("✅ PASS 1 DONE")

if __name__ == "__main__":
    scan()