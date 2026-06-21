import os
import shutil

def mirror():
    if os.path.exists("output_mod"):
        shutil.rmtree("output_mod")

    shutil.copytree("input_extracted", "output_mod")

    print("📁 STRUCTURE MIRRORED")

if __name__ == "__main__":
    mirror()