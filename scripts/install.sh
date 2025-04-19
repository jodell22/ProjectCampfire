#!/bin/bash
# scripts/install.sh - Campfire Install Script

set -e

# 1. Create campfire user if it doesn't exist
if ! id "campfire" &>/dev/null; then
  echo "👤 Creating 'campfire' user..."
  sudo useradd -m -s /bin/bash campfire
fi

# 2. System packages
sudo apt update && sudo apt install -y python3 python3-venv git

# 3. Project location
INSTALL_DIR="/opt/project-campfire"
if [ ! -d "$INSTALL_DIR" ]; then
  sudo git clone https://github.com/jodell22/ProjectCampfire.git "$INSTALL_DIR"
fi
sudo chown -R campfire:campfire "$INSTALL_DIR"

# 4. Switch to campfire user and finish setup
sudo -u campfire bash <<'EOF'
cd /opt/project-campfire

# Set up virtualenv
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
EOF

# 5. Run interactive .env setup only if not already present
if [ ! -f "$INSTALL_DIR/.env" ]; then
  echo "🔑 Starting interactive environment setup..."
  sudo su - campfire -c "python3 /opt/project-campfire/scripts/setup_env.py"
else
  echo "⚠️  Skipping .env setup — already exists at $INSTALL_DIR/.env"
fi

# 6. Systemd service
sudo cp /opt/project-campfire/systemd/campfire.service /etc/systemd/system/
sudo systemctl daemon-reexec
sudo systemctl enable --now campfire.service

echo "✅ Campfire bot installed and running!"
