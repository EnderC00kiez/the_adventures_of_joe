import os
import sys
input("Press any key to continue, and Ctrl+C to exit.")

if sys.platform == "linux" or sys.platform == "darwin":
    os.system('pyinstaller main.py --hidden-import pygame --icon assets/icon.ico --windowed --add-data assets:assets')
elif sys.platform == "win32" or sys.platform == "win64":
    os.system('pyinstaller main.py --hidden-import pygame --icon assets/icon.ico --windowed --add-data assets;assets')
else:
    print("Unknown platform: " + sys.platform)
    sys.exit(1)