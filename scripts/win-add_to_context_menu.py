import os

try:
    from winreg import ConnectRegistry, OpenKey, CreateKey, HKEY_CURRENT_USER, SetValue, SetValueEx, REG_SZ
except OSError:
    print("Could not import 'winreg' - you are probably not on windows.")
    exit(1)

print("This script will add the pylinx upload function into your right-click context menu on Windows.")
input("Press enter to proceed...")

#################
# Find and check all paths for validity
#################
ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPTS_DIR = os.path.realpath(os.path.join(ROOT_DIR, "scripts"))

# Make sure the icon exists
ASSETS_DIR = os.path.realpath(os.path.join(ROOT_DIR, "assets"))
if not os.path.isdir(ASSETS_DIR):
    print("This is an abnormal install - no 'aseets' directory.")
    exit(1)

ASSETS_ICO = os.path.realpath(os.path.join(ASSETS_DIR, "upload-cloud.ico"))
if not os.path.isfile(ASSETS_ICO):
    print("This is an abnormal install - no 'upload-cloud.ico' file.")
    exit(1)

# Make sure there is a powershell script for the context menu
if not os.path.isdir(SCRIPTS_DIR):
    print("This is an abnormal install - no 'scripts' directory.")
    exit(1)

PS_SCRIPT = os.path.realpath(os.path.join(SCRIPTS_DIR, "win-run_from_context_menu.ps1"))
if not os.path.isfile(PS_SCRIPT):
    print("This is an abnormal install - no 'win-run_from_context_menu.ps1' script.")
    exit(1)


command = f"powershell \"{PS_SCRIPT}\" upload \"%1\""

print()
print(f"The default command is\n{command}\n")
print(f"If you really know what you are doing and want to change it "
      f"to a custom command (e.g. you have newer powershell), you can do so here.")

want_custom = input("\t[[E]dit/[C]ontinue with defaults] ").lower() == "e"
if want_custom:
    command = input("Paste your custom command: ")
else:
    print("Continuing with defaults.")

#################
# Create and open registry keys
#################
print("Creating and opening the required registry keys...")
reg = ConnectRegistry(None, HKEY_CURRENT_USER)
shell_key = r"Software\Classes\*\shell"

pylinx_shell_key = r"Software\Classes\*\shell\pylinx"
pylinx_command_key = r"Software\Classes\*\shell\pylinx\command"

reg_pylinx_shell_key = CreateKey(reg, pylinx_shell_key)
reg_pylinx_command_key = CreateKey(reg, pylinx_command_key)

# Edit registry to add an element to the context menu
print("Editing key values...")
SetValueEx(reg_pylinx_shell_key, "", None, REG_SZ, "Upload file with pylinx")

SetValueEx(reg_pylinx_shell_key, "icon", None, REG_SZ, ASSETS_ICO)

SetValueEx(reg_pylinx_command_key, "", None, REG_SZ, command)

# Close all handles
print("Closing key handles...")
reg_pylinx_shell_key.Close()
reg_pylinx_command_key.Close()

reg.Close()

print()
print("=== DONE ===")
print("If you wish to remove pylinx from the context menu, simply delete the key\n"
      r"HKEY_CURRENT_USER\Software\Classes\*\shell\pylinx"
      "\nThis will completely revert everything in this script.")
