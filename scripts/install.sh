#!/bin/bash
# install.sh - Campfire Prep Script

set -e

INSTALL_DIR="/opt/project-campfire"
CAMPFIRE_USER="campfire"

# 1. Create campfire user if it doesn't exist
if ! id "$CAMPFIRE_USER" &>/dev/null; then
  echo "👤 Creating '$CAMPFIRE_USER' user..."
  sudo useradd -m -s /bin/bash $CAMPFIRE_USER
fi

# 2. Install system packages
echo "📦 Installing system dependencies..."
sudo apt update && sudo apt install -y python3 python3-venv git

# 3. Clone project repo
if [ ! -d "$INSTALL_DIR" ]; then
  echo "📁 Cloning Project Campfire..."
  sudo git clone https://github.com/jodell22/ProjectCampfire.git "$INSTALL_DIR"
  sudo chown -R $CAMPFIRE_USER:$CAMPFIRE_USER "$INSTALL_DIR"
else
  echo "📂 Project directory already exists at $INSTALL_DIR"
fi

# 4. Set up Python venv and dependencies
echo "🐍 Setting up Python environment..."
sudo -u $CAMPFIRE_USER python3 -m venv "$INSTALL_DIR/venv"
sudo -u $CAMPFIRE_USER "$INSTALL_DIR/venv/bin/pip" install --upgrade pip
sudo -u $CAMPFIRE_USER "$INSTALL_DIR/venv/bin/pip" install -r "$INSTALL_DIR/requirements.txt"

# 5. Install systemd service
echo "⚙️  Installing systemd service..."
sudo cp "$INSTALL_DIR/systemd/campfire.service" /etc/systemd/system/
sudo systemctl daemon-reexec
sudo systemctl enable campfire.service

# 6. Prompt to run interactive setup
cat <<EOF

🔧 Prep complete. Now switch to the 'campfire' user and finish setup:

    sudo -u campfire python3 /opt/project-campfire/scripts/setup.py

Once complete, run:

    sudo systemctl restart campfire.service

EOF
