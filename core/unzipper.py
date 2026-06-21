import zipfile
import os

def run():
    os.makedirs("input_extracted", exist_ok=True)

    with zipfile.ZipFile("input_zip/ck3_input.zip", 'r') as z:
        z.extractall("input_extracted")

    print("✅ UNZIP DONE")

if __name__ == "__main__":
    run()