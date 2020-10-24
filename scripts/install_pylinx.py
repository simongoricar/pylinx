import os
import sys
from shutil import copy2

REPO = "https://github.com/DefaultSimon/pylinx.git"

print("This script will install linx-pyclient into your current directory.")
print("It is assumed that you have these prerequisites installed and available in your path:\n"
      "\t- git\n"
      "\t- poetry\n"
      "\t- the correct python version\n")

input("If you want to continue, press enter.")

print(f"1) Cloning {REPO}...")
sys.stdout.flush()
os.system(f"git clone {REPO} pylinx")
os.chdir("pylinx")

print("2) Output of poetry --version:")
sys.stdout.flush()
os.system("poetry --version")

print("3) Running 'poetry config --local virtualenvs.in-project true'")
sys.stdout.flush()
os.system("poetry config --local virtualenvs.in-project true")

print("4) Installing packages into a virtualenv")
sys.stdout.flush()
os.system("poetry install")

SCRIPT_DIR_WIN = os.path.realpath(os.path.join(os.path.dirname(os.curdir), ".venv/Scripts"))
SCRIPT_DIR_LINUX = os.path.realpath(os.path.join(os.path.dirname(os.curdir), ".venv/bin"))

CORRECT_SCRIPT_DIR = None
if os.path.isdir(SCRIPT_DIR_WIN):
    CORRECT_SCRIPT_DIR = SCRIPT_DIR_WIN
elif os.path.isdir(SCRIPT_DIR_LINUX):
    CORRECT_SCRIPT_DIR = SCRIPT_DIR_LINUX
else:
    raise Exception("Something went wrong while installing the virtualenv (could not find Scripts/bin directory).")

FINAL_DIR = os.path.realpath(os.path.join(os.path.dirname(os.curdir), "bin"))
if not os.path.isdir(FINAL_DIR):
    os.mkdir(FINAL_DIR)

print("5) Copying pylinx executable")

PYLINX_BINARY = os.path.join(CORRECT_SCRIPT_DIR, "pylinx")
PYLINX_BINARY_EXE = os.path.join(CORRECT_SCRIPT_DIR, "pylinx.exe")
PYLINX_SCRIPT = os.path.join(CORRECT_SCRIPT_DIR, "pylinx-script.py")
PYLINX_SCRIPT_CMD = os.path.join(CORRECT_SCRIPT_DIR, "pylinx.cmd")

if os.path.isfile(PYLINX_BINARY):
    print(f"Copying '{PYLINX_BINARY}' to '{FINAL_DIR}'")
    copy2(PYLINX_BINARY, FINAL_DIR)

if os.path.isfile(PYLINX_BINARY_EXE):
    print(f"Copying '{PYLINX_BINARY_EXE}' to '{FINAL_DIR}'")
    copy2(PYLINX_BINARY_EXE, FINAL_DIR)

if os.path.isfile(PYLINX_SCRIPT):
    print(f"Copying '{PYLINX_SCRIPT}' to '{FINAL_DIR}'")
    copy2(PYLINX_SCRIPT, FINAL_DIR)

if os.path.isfile(PYLINX_SCRIPT_CMD):
    print(f"Copying '{PYLINX_SCRIPT_CMD}' to '{FINAL_DIR}'")
    copy2(PYLINX_SCRIPT_CMD, FINAL_DIR)

os.chdir("..")
if os.path.isfile("install_pylinx.py"):
    os.remove("install_pylinx.py")

print("\n== DONE! ==")
print("To finish the installation, please add the following path to your PATH variable:\n")
print(FINAL_DIR.center(82))
print("\nAfterwards, the binary 'pylinx'/'pylinx.exe' will be available")
