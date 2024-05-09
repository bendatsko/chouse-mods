import os
import subprocess
import sys
import shutil
import platform
from pathlib import Path
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

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

# Dependencies required for the script
REQUIRED_LIBRARIES = {
    'watchdog': 'watchdog',
    'win10toast': 'win10toast',
    'macos-notifications': 'macos-notifications'
}

# Install required libraries
def install_and_import(package_name, import_name=None):
    import_name = import_name or package_name
    try:
        __import__(import_name)
    except ImportError:
        print(f"[INFO] Installing '{package_name}'...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"[INFO] '{package_name}' installed successfully.")
        __import__(import_name)

# Install all required dependencies
def install_dependencies():
    os_name = platform.system()
    install_and_import('watchdog')
    if os_name == "Windows":
        install_and_import('win10toast')
    elif os_name == "Darwin":  # macOS
        install_and_import('macos-notifications')

# Notification function
def notify_user(title, message):
    os_name = platform.system()
    try:
        if os_name == "Windows":
            from win10toast import ToastNotifier
            toaster = ToastNotifier()
            toaster.show_toast(title, message, duration=5)
        elif os_name == "Darwin":  # macOS
            from mac_notifications import client
            client.send(message=message, title=title, subtitle="Minecraft Mod Updater")
        else:
            print(f"[INFO] Notifications not supported on {os_name}.")
    except ImportError:
        print(f"[ERROR] Notification library not found for {os_name}. Please install the required library.")
        if os_name == "Windows":
            print("Install it with `pip install win10toast`.")
        elif os_name == "Darwin":
            print("Install it with `pip install macos-notifications`.")

# Clone or update the repository
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

# Replace the mods folder
def replace_mods_folder():
    if MODS_FOLDER_PATH.exists():
        if TARGET_MODS_FOLDER.exists():
            print(f"[INFO] Removing existing '{TARGET_MODS_FOLDER}' folder...")
            shutil.rmtree(TARGET_MODS_FOLDER)
        print(f"[INFO] Copying '{MODS_FOLDER_PATH}' to '{TARGET_MODS_FOLDER}'...")
        shutil.copytree(MODS_FOLDER_PATH, TARGET_MODS_FOLDER)
        print("[INFO] Mods folder updated successfully!")
        notify_user("Mods Update", "Your mods folder has been updated successfully!")
    else:
        print(f"[ERROR] Mods folder not found in the repository at {MODS_FOLDER_PATH}.")
        notify_user("Mods Update Error", f"Mods folder not found in the repository at {MODS_FOLDER_PATH}.")

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
    install_dependencies()
    monitor_minecraft_instance()

# b