#!/usr/bin/env python3

import os

print("\n🔧 Nova Setup Wizard")
print("------------------------")

INSTALL_DIR = "/opt/project-campfire"
ENV_FILE = os.path.join(INSTALL_DIR, ".env")

# 1. Collect and write environment configuration
print("\nPlease enter the required configuration values:")

bot_token = input("Discord Bot Token: ").strip()
openai_key = input("OpenAI API Key: ").strip()
dm_room = input("DM Room Channel ID: ").strip()
world_room = input("World Channel ID: ").strip()

with open(ENV_FILE, "w") as f:
    f.write(f"DISCORD_BOT_TOKEN={bot_token}\n")
    f.write(f"OPENAI_API_KEY={openai_key}\n")
    f.write(f"DM_ROOM_CHANNEL_ID={dm_room}\n")
    f.write(f"WORLD_CHANNEL_ID={world_room}\n")

print("\n✅ .env file created at /opt/project-campfire/.env")
print("You can now start or restart the Campfire bot using:")
print("    sudo systemctl restart campfire.service")

print("\n🎉 Setup complete! Nova is ready to serve.")
