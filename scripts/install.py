#!/usr/bin/env python3

import os
import subprocess

print("\n🔧 Nova Installer")
print("-----------------")

INSTALL_DIR = "/opt/project-campfire"
ENV_FILE = os.path.join(INSTALL_DIR, ".env")

# 1. Ensure campfire user exists
if subprocess.call(["id", "campfire"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
    print("👤 Creating 'campfire' user...")
    subprocess.run(["sudo", "useradd", "-m", "-s", "/bin/bash", "campfire"], check=True)

# 2. Install required packages
print("📦 Installing system packages...")
subprocess.run(["sudo", "apt", "update"], check=True)
subprocess.run(["sudo", "apt", "install", "-y", "python3", "python3-venv", "git"], check=True)

# 3. Clone project if not present
if not os.path.isdir(INSTALL_DIR):
    print("📁 Cloning Project Campfire...")
    subprocess.run(["sudo", "git", "clone", "https://github.com/jodell22/ProjectCampfire.git", INSTALL_DIR], check=True)
subprocess.run(["sudo", "chown", "-R", "campfire:campfire", INSTALL_DIR], check=True)

# 4. Setup Python environment
print("🐍 Setting up virtual environment...")
subprocess.run(["sudo", "-u", "campfire", "python3", "-m", "venv", os.path.join(INSTALL_DIR, "venv")], check=True)
subprocess.run(["sudo", "-u", "campfire", os.path.join(INSTALL_DIR, "venv", "bin", "pip"), "install", "--upgrade", "pip"], check=True)
subprocess.run(["sudo", "-u", "campfire", os.path.join(INSTALL_DIR, "venv", "bin", "pip"), "install", "-r", os.path.join(INSTALL_DIR, "requirements.txt")], check=True)

# 5. Run interactive .env setup if missing
if not os.path.isfile(ENV_FILE):
    print("🔑 Let's configure your bot environment...")
    token = input("Discord Bot Token: ")
    api_key = input("OpenAI API Key: ")
    dm_id = input("DM Room Channel ID: ")
    world_id = input("World Channel ID: ")

    with open("/tmp/.env", "w") as f:
        f.write(f"DISCORD_BOT_TOKEN={token}\n")
        f.write(f"OPENAI_API_KEY={api_key}\n")
        f.write(f"DM_ROOM_CHANNEL_ID={dm_id}\n")
        f.write(f"WORLD_CHANNEL_ID={world_id}\n")

    subprocess.run(["sudo", "mv", "/tmp/.env", ENV_FILE], check=True)
    subprocess.run(["sudo", "chown", "campfire:campfire", ENV_FILE], check=True)
else:
    print(f"⚠️  Skipping .env setup — already exists at {ENV_FILE}")

# 6. Systemd service
print("⚙️  Enabling systemd service...")
subprocess.run(["sudo", "cp", os.path.join(INSTALL_DIR, "systemd", "campfire.service"), "/etc/systemd/system/"], check=True)
subprocess.run(["sudo", "systemctl", "daemon-reexec"], check=True)
subprocess.run(["sudo", "systemctl", "enable", "campfire.service"], check=True)
subprocess.run(["sudo", "systemctl", "restart", "campfire.service"], check=True)

print("\n✅ Campfire bot installed and running!")
