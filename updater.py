import os
import subprocess
import sys
import platform
from pathlib import Path
import shutil
import time

# Constants
GITHUB_REPO_URL = "https://github.com/bendatsko/chouse-mods.git"
REPO_NAME = "chouse-mods"
SCRIPT_DIR = Path(__file__).parent
INSTANCE_FILE = SCRIPT_DIR / "minecraftinstance.json"
LOCAL_REPO_PATH = SCRIPT_DIR / REPO_NAME
MODS_FOLDER_PATH = LOCAL_REPO_PATH / "MODS"
TARGET_MODS_FOLDER = SCRIPT_DIR / "mods"
COOLDOWN_PERIOD = 60  # in seconds
last_pull_time = 0

# Dependencies (requirements.txt content)
REQUIREMENTS = """
watchdog==4.0.0
win10toast==0.9
macos-notifications==0.1.4
"""

# Install requirements.txt from multi-line string because I'm lazy
def install_requirements():
    requirements = REQUIREMENTS.strip().splitlines()
    for requirement in requirements:
        package_spec = requirement.split(';')[0].strip()
        try:
            # Attempt to import the package directly
            __import__(package_spec.split('==')[0].replace('-', '_'))
        except ImportError:
            # Install via pip if not already available
            try:
                print(f"[INFO] Installing '{package_spec}'...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", requirement])
                print(f"[INFO] '{package_spec}' installed successfully.")
            except subprocess.CalledProcessError as e:
                print(f"[ERROR] Failed to install '{package_spec}': {e}. Continuing...")

install_requirements()

# Import libraries
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

try:
    from win10toast import ToastNotifier  # For Windows notifications
except ImportError:
    ToastNotifier = None

try:
    from mac_notifications import client as mac_client  # For macOS notifications
except ImportError:
    mac_client = None



# Clone/update mod folder repository
def update_repo():
    global last_pull_time
    current_time = time.time()
    if current_time - last_pull_time < COOLDOWN_PERIOD:
        print(f"[INFO] Skipping pull due to cooldown. Please wait {int(COOLDOWN_PERIOD - (current_time - last_pull_time))} seconds.")
        return
    last_pull_time = current_time

    if not LOCAL_REPO_PATH.exists():
        # Clone the repository
        print("[INFO] Cloning the repository...")
        subprocess.run(['git', 'clone', GITHUB_REPO_URL, str(LOCAL_REPO_PATH)], check=True)
    else:
        # Pull the latest changes
        print("[INFO] Pulling the latest changes from the repository...")
        subprocess.run(['git', '-C', str(LOCAL_REPO_PATH), 'pull'], check=True)

# Replace mods folder
def replace_mods_folder():
    if MODS_FOLDER_PATH.exists():
        if TARGET_MODS_FOLDER.exists():
            print(f"[INFO] Removing existing '{TARGET_MODS_FOLDER}' folder...")
            shutil.rmtree(TARGET_MODS_FOLDER)
        print(f"[INFO] Copying '{MODS_FOLDER_PATH}' to '{TARGET_MODS_FOLDER}'...")
        shutil.copytree(MODS_FOLDER_PATH, TARGET_MODS_FOLDER)
        print("[INFO] Mods folder updated successfully!")
    else:
        print(f"[ERROR] Mods folder not found in the repository at {MODS_FOLDER_PATH}.")

# Event handler class
class MinecraftInstanceEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path == str(INSTANCE_FILE):
            print(f"[INFO] '{INSTANCE_FILE}' was modified!")
            update_repo()
            replace_mods_folder()

# Watchdog observer
def monitor_minecraft_instance():
    # Check if the minecraftinstance.json file exists
    if not INSTANCE_FILE.exists():
        print(f"[ERROR] {INSTANCE_FILE} not found in {SCRIPT_DIR}. Please ensure the file is present.")
        return

    event_handler = MinecraftInstanceEventHandler()
    observer = Observer()
    observer.schedule(event_handler, str(SCRIPT_DIR), recursive=False)
    observer.start()
    print(f"[INFO] Watching for changes to 'minecraftinstance.json' in {SCRIPT_DIR}...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# Run the updater
if __name__ == "__main__":
    monitor_minecraft_instance()
