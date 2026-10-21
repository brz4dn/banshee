import os
import sys
import time
import uuid
import json
import socket
import platform
import subprocess
import webbrowser
from datetime import datetime

# Import the device management backend protocol buffer module
try:
    import device_management_backend_pb2
except ImportError:
    pass

VERSION = "1.00"
DEV = "brz4dn"
WEBSITE = "https://guns.lol/brz4dn"

OAUTH_CLIENT_ID = "77185425425430.apps.googleusercontent.com"
OAUTH_CLIENT_SECRET = "OTJgUOQcT7lO7GsGZq2G4IlT"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_DIR = os.path.join(SCRIPT_DIR, ".banshee-venv")
PACKAGES = ["protobuf", "requests", "google"]
W = 60  # Perfectly fitted width for the banner layout

BANNER_LINES = [
    " ▀▀▀██▄                         ░░░                   ",
    "░░░ ███                         ▒▒▒                   ",
    "▒▒▒ ███                         ▓▓▓                   ",
    "▓▓▓▄██▀ ▄██▀██▄ ███▀██▄ ▄██▀██▄ ███▀██▄ ▄██▀██▄ ▄██▀██▄",
    "███ ███ ███ ███ ███ ███ ███ ███ ███ ███ ███ ███ ███ ███",
    "███ ███  ▄▄▄███ ███ ███ ▀██▄▄▄  ███ ███ ███▀▀▀▀ ███▀▀▀▀",
    "███ ███ ███ ███ ███ ███ ▄▄▄ ███ ███ ███ ███ ███ ███ ███",
    "███ ███ ███ ███ ███ ███ ███ ███ ███ ███ ███ ███ ███ ███",
    "███▄██▀ ▀██▄███ ███ ███ ▀██▄██▀ ███ ███ ▀██▄██▀ ▀██▄██▀",
    "        ▀█     █▀   █▀      █▀    █▀      █▀   ",
    "        ▄     ▄     ▄       ▄     ▄       ▄    ",
]

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.5)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def paint(text, color_code="97"):
    return f"\033[{color_code}m\033[1m{text}\033[0m"

def say(msg="", end="\n", delay=0.01):
    for char in msg:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(end)
    sys.stdout.flush()

def animated_loader(msg="Processing"):
    sys.stdout.write(paint(f"[*] {msg} "))
    for _ in range(3):
        for char in "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏":
            sys.stdout.write(paint(char))
            sys.stdout.flush()
            time.sleep(0.05)
            sys.stdout.write("\b")
    sys.stdout.write(paint("Done!\n", "97"))

def _pad(line, inner):
    if len(line) >= inner:
        return line[:inner]
    return line + " " * (inner - len(line))

def build_rows():
    inner = W - 2
    rows = [("top", None)]
    
    for ln in BANNER_LINES:
        rows.append(("text", _pad(f" {ln}", inner)))
    
    rows.append(("div", f"Banshee v{VERSION} | Dev: {DEV}"))

    info = [
        ("User", "username202678910"), 
        ("IP", get_ip()), 
        ("System", platform.system()),
    ]
    for k, v in info:
        rows.append(("text", _pad(f"  {k:<8}: {v}", inner)))

    rows.append(("div", "CONTROL PANEL"))
    menu_items = [
        "[1] Install Google Requests", 
        "[2] Device Enrollment Signup", 
        "[3] Unenroll The Device", 
        "[4] Open Official Website", 
        "[0] Exit Toolkit"
    ]
    for item in menu_items:
        rows.append(("text", _pad(f"  {item}", inner)))

    rows.append(("bottom", None))
    return rows

def make_line(kind, body):
    if kind == "top":
        return paint("╔" + "═" * (W - 2) + "╗", "97")
    if kind == "bottom":
        return paint("╚" + "═" * (W - 2) + "╝", "97")
    if kind == "div":
        label = f" {body} "
        side = (W - 2 - len(label)) // 2
        return paint("╠" + "─" * side + label + "─" * (W - 2 - side - len(label)) + "╣", "97")
    return paint("║", "97") + body + paint("║", "97")

def draw_shell():
    clear()
    sys.stdout.write("\n")
    for kind, body in build_rows():
        sys.stdout.write(make_line(kind, body) + "\n")
    sys.stdout.write("\n")

def prompt():
    user = "username202678910"
    cwd = "/home/username/banshee"
    prompt_top = paint(f"┌──({user}@banshee)", "97") + paint("─", "97") + paint(f"[{cwd}]", "97")
    prompt_bottom = paint("└─$ ", "97")
    
    sys.stdout.write(f"{prompt_top}\n{prompt_bottom}")
    sys.stdout.flush()
    try:
        return input().strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return "0"

def in_venv():
    return sys.prefix != sys.base_prefix

def venv_python():
    if os.name == "nt":
        return os.path.join(VENV_DIR, "Scripts", "python.exe")
    return os.path.join(VENV_DIR, "bin", "python")

def install_google():
    say("\n[*] Initializing Package Installer...")
    animated_loader("Setting up environment")
    if in_venv():
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", *PACKAGES], check=True)
            say(paint("[+] Packages installed successfully.", "97"))
        except subprocess.CalledProcessError as e:
            say(paint(f"[-] Installation Failed: {e}", "97"))
        return
    
    if not os.path.exists(venv_python()):
        try:
            subprocess.run([sys.executable, "-m", "venv", VENV_DIR], check=True)
        except subprocess.CalledProcessError:
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", *PACKAGES, "--break-system-packages"], check=True)
                say(paint("[+] Installed globally with system override.", "97"))
                return
            except subprocess.CalledProcessError as e:
                say(paint(f"[-] Install Failed: {e}", "97"))
                return
    try:
        subprocess.run([venv_python(), "-m", "pip", "install", *PACKAGES], check=True)
        say(paint("[+] Done.", "97"))
    except subprocess.CalledProcessError as e:
        say(paint(f"[-] Install Failed: {e}", "97"))
    time.sleep(1)

def device_enrollment_signup():
    url = "https://accounts.google.com/v3/signin/identifier?flow=deviceEnrollment&flowName=GlifSetupChromeOs"
    say(paint(f"\n[*] Opening Device Enrollment Signup page...", "97"))
    webbrowser.open(url)
    time.sleep(1)
    
    say(paint("\n==================================================", "97"))
    say(paint("             ENROLLMENT INSTRUCTIONS              ", "97"))
    say(paint("==================================================", "97"))
    say(paint(" 1. Enter your School Email and Login", "97"))
    say(paint(" 2. Inspect when the Site Crashes", "97"))
    say(paint(" 3. Go to DevTools > Application", "97"))
    say(paint(" 4. Find \"Accounts.Google.Com\" and Find \"Oauth\"", "97"))
    say(paint(" 5. Enter the Oauth Code in here and Continue", "97"))
    say(paint("==================================================", "97"))

def unenroll_device():
    say(paint("\n[*] Running Unenroll...", "97"))
    try:
        import requests
    except ImportError as e:
        say(paint(f"[-] Missing Package ({e}). Use Option [ 1 ] First.", "97"))
        return
    try:
        import device_management_backend_pb2 as pb
    except ImportError as e:
        say(paint(f"[-] Missing Protocol Buffer Module ({e}).", "97"))
        return
    
    try:
        serial_number = input(paint("Serial Number: ")).strip()
        oauth_code = input(paint("Oauth Code: ")).strip()
    except (EOFError, KeyboardInterrupt):
        say(paint("\n[-] Unenroll Canceled.", "97"))
        return
        
    say(paint("[*] Contacting Google...", "97"))
    try:
        r = requests.post("https://www.googleapis.com/oauth2/v4/token", data={
            "code": oauth_code, "client_id": OAUTH_CLIENT_ID,
            "client_secret": OAUTH_CLIENT_SECRET,
            "grant_type": "authorization_code"}, timeout=15)
        r.raise_for_status()
        refresh_token = r.json()["refresh_token"]
        r = requests.post("https://www.googleapis.com/oauth2/v4/token", data={
            "client_id": OAUTH_CLIENT_ID, "client_secret": OAUTH_CLIENT_SECRET,
            "grant_type": "refresh_token", "refresh_token": refresh_token,
            "scope": "https://www.googleapis.com/auth/chromeosdevicemanagement "
                     "https://www.googleapis.com/auth/userinfo.email"}, timeout=15)
        r.raise_for_status()
        oauth_token = r.json()["access_token"]
        device_id = str(uuid.uuid4())

        reg = pb.DeviceRegisterRequest()
        reg.type = pb.DeviceRegisterRequest.DEVICE
        reg.machine_id = serial_number
        req = pb.DeviceManagementRequest()
        req.register_request.CopyFrom(reg)

        r = requests.post(
            f"https://m.google.com/devicemanagement/data/api?devicetype=2"
            f"&apptype=Chrome&request=register&deviceid={device_id}"
            f"&oauth_token={oauth_token}",
            headers={"Content-Type": "application/protobuf"},
            data=req.SerializeToString(), timeout=15)
        data = pb.DeviceManagementResponse()
        data.ParseFromString(r.content)
        if data.error_message:
            say(paint(f"[-] Registration Error: {data.error_message}", "97"))
            return
        dmtoken = data.register_response.device_management_token

        pf = pb.PolicyFetchRequest()
        pf.policy_type = "google/chromeos/device"
        sk = pb.DeviceStateKeyUpdateRequest()
        for _ in range(5):
            sk.server_backed_state_keys.append(os.urandom(32))
        req = pb.DeviceManagementRequest()
        req.policy_request.requests.append(pf)
        req.device_state_key_update_request.CopyFrom(sk)

        r = requests.post(
            f"https://m.google.com/devicemanagement/data/api?retry=false"
            f"&apptype=Chrome&deviceid={device_id}&devicetype=2&request=policy",
            headers={"Authorization": f"GoogleDMToken token={dmtoken}",
                     "Content-Type": "application/protobuf"},
            data=req.SerializeToString(), timeout=15)
        data = pb.DeviceManagementResponse()
        data.ParseFromString(r.content)
        say(paint("[+] Response:", "97"))
        print(data)
    except Exception as e:
        say(paint(f"[-] Error: {e}", "97"))

def open_website():
    say(paint(f"\n[*] Launching browser to {WEBSITE} ...", "97"))
    webbrowser.open(WEBSITE)

def main():
    draw_shell()
    while True:
        choice = prompt()
        if choice in ("clear", "cls"):
            draw_shell()
            continue
        if choice == "1":
            install_google()
        elif choice == "2":
            device_enrollment_signup()
        elif choice == "3":
            unenroll_device()
        elif choice == "4":
            open_website()
        elif choice == "0":
            say(paint("\nExiting Banshee...", "97"))
            break
        elif choice == "":
            continue
        else:
            say(paint("[-] Invalid Option.", "97"))
            continue
        
        if choice != "0":
            time.sleep(1.5)
            draw_shell()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        say(paint("Exiting Banshee...", "97"))
