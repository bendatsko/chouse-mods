import os
import subprocess
from pathlib import Path
import shutil

# Constants
GITHUB_REPO_URL = "https://github.com/bendatsko/chouse-mods.git"
REPO_NAME = "chouse-mods"
SCRIPT_DIR = Path(__file__).parent
LOCAL_REPO_PATH = SCRIPT_DIR / REPO_NAME
MODS_FOLDER_PATH = LOCAL_REPO_PATH / "MODS"
TARGET_MODS_FOLDER = SCRIPT_DIR / "mods"

BANNER = """
############################################
#                                          #
#        CHouse Server Mod Updater         #
#                                          #
############################################
"""

# clone/update mod folder repository
def update_repo():
    if not LOCAL_REPO_PATH.exists():
        # Clone the repository
        print("[INFO] Cloning the repository...")
        subprocess.run(['git', 'clone', GITHUB_REPO_URL, str(LOCAL_REPO_PATH)], check=True)
    else:
        # Pull the latest changes
        print("[INFO] Pulling the latest changes from the repository...")
        subprocess.run(['git', '-C', str(LOCAL_REPO_PATH), 'pull'], check=True)

# replace mods folder
def replace_mods_folder():
    if MODS_FOLDER_PATH.exists():
        if TARGET_MODS_FOLDER.exists():
            print(f"[INFO] Removing existing '{TARGET_MODS_FOLDER}' folder...")
            shutil.rmtree(TARGET_MODS_FOLDER)
        print(f"[INFO] Copying mods from '{MODS_FOLDER_PATH}' to '{TARGET_MODS_FOLDER}'...")
        shutil.copytree(MODS_FOLDER_PATH, TARGET_MODS_FOLDER)
        print("[INFO] Mods folder updated successfully!")
    else:
        print(f"[ERROR] Mods folder not found in the repository at {MODS_FOLDER_PATH}.")

if __name__ == "__main__":
    print(BANNER)
    update_repo()
    replace_mods_folder()
    print("\n[INFO] Update complete.\n")
    input("Press any key to exit...")
