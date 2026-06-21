import os

print("🚀 START CK3 TRANSLATOR")

os.system("python core/unzipper.py")
os.system("python core/global_scan.py")
os.system("python core/file_mirror.py")
os.system("python core/pipeline.py")

print("✅ DONE - MOD READY")