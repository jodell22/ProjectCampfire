#!/usr/bin/env python3

import os

print("\n🔧 Nova Environment Setup")
print("--------------------------")

bot_token = input("Discord Bot Token: ")
openai_key = input("OpenAI API Key: ")
dm_channel = input("DM Room Channel ID: ")
world_channel = input("World Channel ID: ")

env_path = "/opt/project-campfire/.env"

with open(env_path, "w") as f:
    f.write(f"DISCORD_BOT_TOKEN={bot_token}\n")
    f.write(f"OPENAI_API_KEY={openai_key}\n")
    f.write(f"DM_ROOM_CHANNEL_ID={dm_channel}\n")
    f.write(f"WORLD_CHANNEL_ID={world_channel}\n")

print("\n✅ .env file created at /opt/project-campfire/.env")

print("\n🔁 Restarting Nova bot service...")
os.system("sudo systemctl restart campfire.service")

print("\n✅ Setup complete. Nova is live!")
