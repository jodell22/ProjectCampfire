#!/usr/bin/env python3

import os
import db.database  # triggers DB creation on import

print("\n🔧 Nova Setup Wizard")
print("------------------------")

INSTALL_DIR = "/opt/project-campfire"
ENV_FILE = os.path.join(INSTALL_DIR, ".env")

# Load existing values if they exist
existing = {}
if os.path.exists(ENV_FILE):
    with open(ENV_FILE, "r") as f:
        for line in f:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                existing[key] = value

# Helper function for prompts with defaults
def prompt(field, key):
    default = existing.get(key, "")
    if default:
        return input(f"{field} [{default}]: ").strip() or default
    return input(f"{field}: ").strip()

print("\nYou can press Enter to keep the current value if it exists.")

bot_token = prompt("Discord Bot Token", "DISCORD_BOT_TOKEN")
openai_key = prompt("OpenAI API Key", "OPENAI_API_KEY")
dm_room = prompt("DM Room Channel ID", "DM_ROOM_CHANNEL_ID")
world_room = prompt("World Channel ID", "WORLD_CHANNEL_ID")

with open(ENV_FILE, "w") as f:
    f.write(f"DISCORD_BOT_TOKEN={bot_token}\n")
    f.write(f"OPENAI_API_KEY={openai_key}\n")
    f.write(f"DM_ROOM_CHANNEL_ID={dm_room}\n")
    f.write(f"WORLD_CHANNEL_ID={world_room}\n")

print("\n✅ .env file created at /opt/project-campfire/.env")
print("You can now start or restart the Campfire bot using:")
print("    sudo systemctl restart campfire.service")

print("\n🎉 Setup complete! Nova is ready to serve.")
