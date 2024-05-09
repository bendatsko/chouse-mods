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

# Dependencies (requirements.txt content)
REQUIREMENTS = """
aiohttp==3.9.3
aiosignal==1.3.1
annotated-types==0.6.0
async-generator==1.10
async-timeout==4.0.3
asynctest==0.13.0
attrs==23.2.0
av==11.0.0
beautifulsoup4==4.12.2
black==23.3.0
blis==0.7.11
CacheControl==0.13.1
cachetools==5.3.0
catalogue==2.0.10
certifi==2024.2.2
cffi==1.15.1
cfgv==3.3.1
chardet==5.1.0
charset-normalizer==3.3.2
click==8.1.7
cloudpathlib==0.16.0
colorama==0.4.6
coloredlogs==15.0.1
confection==0.1.4
contourpy==1.2.1
coverage==7.2.3
cryptography==41.0.4
cssselect==1.2.0
ctranslate2==4.1.0
cycler==0.12.1
cymem==2.0.8
distlib==0.3.6
dnspython==2.3.0
docker==6.0.1
duckduckgo-search==2.8.6
en-core-web-sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1-py3-none-any.whl#sha256=86cc141f63942d4b2c5fcee06630fd6f904788d2f0ab005cce45aadb8fb73889
exceptiongroup==1.1.1
faster-whisper==1.0.1
ffmpeg-python==0.2.0
filelock==3.12.4
firebase-admin==6.2.0
flake8==6.0.0
Flask==2.2.2
Flask-Cors==4.0.0
flatbuffers==24.3.25
fonttools==4.51.0
frozenlist==1.4.1
fsspec==2023.9.2
future==1.0.0
gitdb==4.0.10
GitPython==3.1.31
google-api-core==2.11.0
google-api-python-client==2.86.0
google-auth==2.17.3
google-auth-httplib2==0.1.0
google-cloud-core==2.3.3
google-cloud-firestore==2.12.0
google-cloud-storage==2.11.0
google-crc32c==1.5.0
google-resumable-media==2.6.0
googleapis-common-protos==1.59.0
grpcio==1.59.0
grpcio-status==1.59.0
gTTS==2.3.1
h11==0.14.0
httplib2==0.22.0
huggingface-hub==0.22.2
humanfriendly==10.0
identify==2.5.23
idna==3.6
iniconfig==2.0.0
isort==5.12.0
itsdangerous==2.1.2
Jinja2==3.1.3
joblib==1.3.2
jsonschema==4.17.3
kiwisolver==1.4.5
langcodes==3.3.0
llamaapi==0.1.36
loguru==0.7.0
lxml==4.9.2
MarkupSafe==2.1.5
matplotlib==3.8.4
mccabe==0.7.0
mpmath==1.3.0
msgpack==1.0.7
multidict==6.0.5
murmurhash==1.0.10
mypy-extensions==1.0.0
nest-asyncio==1.6.0
networkx==3.2
nltk==3.8.1
nodeenv==1.7.0
numpy==1.26.4
oauthlib==3.2.2
onnxruntime==1.17.1
openai==0.27.2
opencv-contrib-python==4.9.0.80
opencv-python==4.9.0.80
orjson==3.8.10
outcome==1.2.0
packaging==24.0
pandas==2.2.1
pathspec==0.11.1
pathy==0.10.1
pdf2image==1.16.3
pillow==10.3.0
pinecone-client==2.2.1
platformdirs==3.4.0
playsound==1.2.2
pluggy==1.0.0
plyer==2.1.0
praw==7.7.1
prawcore==2.4.0
pre-commit==3.2.2
preshed==3.0.9
proto-plus==1.22.3
protobuf==4.22.3
psutil==5.9.8
py-cpuinfo==9.0.0
pyasn1==0.5.0
pyasn1-modules==0.3.0
pycodestyle==2.10.0
pycparser==2.21
pydantic==2.6.4
pydantic_core==2.16.3
pyflakes==3.0.1
pygame==2.5.2
PyJWT==2.8.0
pyparsing==3.1.2
pypiwin32==223
pyreadline3==3.4.1
pyrsistent==0.19.3
PySocks==1.7.1
pytest==7.3.1
pytest-asyncio==0.21.0
pytest-benchmark==4.0.0
pytest-cov==4.0.0
pytest-integration==0.2.3
pytest-mock==3.10.0
python-dateutil==2.9.0.post0
python-dotenv==1.0.1
pytz==2024.1
pywin32==306
PyYAML==6.0
readability-lxml==0.8.1
redis==4.5.4
regex==2023.12.25
requests==2.31.0
requests-oauthlib==1.3.1
rsa==4.9
safetensors==0.4.2
selenium==4.19.0
six==1.16.0
smart-open==6.4.0
smbus2==0.4.3
smmap==5.0.0
sniffio==1.3.0
sortedcontainers==2.4.0
soupsieve==2.4.1
spacy==3.7.4
spacy-legacy==3.0.12
spacy-loggers==1.0.5
spacytextblob==4.0.0
sparkfun-pi-servo-hat==0.9.0
sparkfun-qwiic-pca9685==0.9.1
sparkfun_qwiic_i2c==1.0.0
srsly==2.4.8
sympy==1.12
textblob==0.15.3
thinc==8.2.3
tiktoken==0.3.3
tokenizers==0.15.2
tomli==2.0.1
torch==2.0.0
torchaudio==2.0.1
torchvision==0.16.0
tqdm==4.66.2
transformers==4.39.3
trio==0.22.0
trio-websocket==0.10.2
tweepy==4.14.0
typer==0.9.4
typing_extensions==4.11.0
tzdata==2024.1
update-checker==0.18.0
uritemplate==4.1.1
urllib3==2.2.1
virtualenv==20.22.0
wasabi==1.1.2
watchdog==4.0.0
weasel==0.3.4
webdriver-manager==3.8.6
websocket-client==1.7.0
Werkzeug==2.2.2
win10toast==0.9
win32-setctime==1.1.0
wsproto==1.2.0
yarl==1.9.4
"""

# Install required libraries from the embedded requirements
def install_requirements():
    requirements = REQUIREMENTS.strip().splitlines()
    for requirement in requirements:
        package_spec = requirement.split(';')[0].strip()
        try:
            __import__(package_spec.split('==')[0].replace('-', '_'))
        except ImportError:
            print(f"[INFO] Installing '{package_spec}'...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", requirement])
            print(f"[INFO] '{package_spec}' installed successfully.")

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
    install_requirements()
    monitor_minecraft_instance()
