import os
import sys
from shutil import copy2

REPO = "https://github.com/DefaultSimon/linx-pyclient.git"

print("This script will install linx-pyclient into your current directory.")
print("It is assumed that you have these prerequisites installed and available in your path:\n"
      "\t- git\n"
      "\t- poetry\n"
      "\t- the correct python version\n")

input("If you want to continue, press enter.")

print(f"1) Cloning {REPO}...")
sys.stdout.flush()
os.system(f"git clone {REPO} linx-pyclient")
os.chdir("linx-pyclient")

print("2) Output of poetry --version:")
sys.stdout.flush()
os.system("poetry --version")

print("3) Running 'poetry config --local virtualenvs.in-project true'")
sys.stdout.flush()
os.system("poetry config --local virtualenvs.in-project true")

print("4) Installing packages into a virtualenv")
sys.stdout.flush()
os.system("poetry install")

SCRIPT_DIR = os.path.realpath(os.path.join(os.path.dirname(os.curdir), ".venv/Scripts"))
FINAL_DIR = os.path.realpath(os.path.join(os.path.dirname(os.curdir), "bin"))
if not os.path.isdir(SCRIPT_DIR):
    raise Exception("Something went wrong while installing the virtualenv.")
if not os.path.isdir(FINAL_DIR):
    os.mkdir(FINAL_DIR)

print("5) Copying pylinx executable")

PYLINX_BINARY = os.path.join(SCRIPT_DIR, "pylinx")
PYLINX_BINARY_EXE = os.path.join(SCRIPT_DIR, "pylinx.exe")
PYLINX_SCRIPT = os.path.join(SCRIPT_DIR, "pylinx-script.py")

if os.path.isfile(PYLINX_BINARY):
    print(f"Copying '{PYLINX_BINARY}' to '{FINAL_DIR}'")
    copy2(PYLINX_BINARY, FINAL_DIR)

if os.path.isfile(PYLINX_BINARY_EXE):
    print(f"Copying '{PYLINX_BINARY_EXE}' to '{FINAL_DIR}'")
    copy2(PYLINX_BINARY_EXE, FINAL_DIR)

if os.path.isfile(PYLINX_SCRIPT):
    print(f"Copying '{PYLINX_SCRIPT}' to '{FINAL_DIR}'")
    copy2(PYLINX_SCRIPT, FINAL_DIR)

print("\n== DONE! ==")
print("To finish the installation, please add the following path to your PATH variable:\n")
print(FINAL_DIR.center(82))
print("\nAfterwards, the binary 'pylinx'/'pylinx.exe' will be available")
