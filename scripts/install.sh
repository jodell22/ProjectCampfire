#!/bin/bash
# scripts/install.sh - Campfire Install Script

set -e

# 1. System packages
sudo apt update && sudo apt install -y python3 python3-venv git

# 2. Project location
INSTALL_DIR="/opt/project-campfire"
if [ ! -d "$INSTALL_DIR" ]; then
  sudo git clone https://github.com/jodell22/ProjectCampfire.git "$INSTALL_DIR"
fi
cd "$INSTALL_DIR"

# 3. Set permissions (optional customization)
sudo chown -R $(whoami):$(whoami) "$INSTALL_DIR"

# 4. Python virtual environment
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 5. Environment config
echo ""
echo "🔑 Let's set up your .env file."

read -p "Discord Bot Token: " discord_token
read -p "OpenAI API Key: " openai_key
read -p "DM Room Channel ID: " dm_channel
read -p "World Channel ID: " world_channel

cat > .env <<EOF
DISCORD_BOT_TOKEN=$discord_token
OPENAI_API_KEY=$openai_key
DM_ROOM_CHANNEL_ID=$dm_channel
WORLD_CHANNEL_ID=$world_channel
EOF

echo "✅ .env file created!"

# 6. Systemd service
sudo cp systemd/campfire.service /etc/systemd/system/
sudo systemctl daemon-reexec
sudo systemctl enable --now campfire.service

echo "✅ Campfire bot installed and running!"
