#!/bin/bash
set -e

INSTALL_DIR="/opt/project-campfire"
cd "$INSTALL_DIR"

# Pull latest changes
echo "🔄 Pulling latest changes..."
git pull

# Activate venv and update deps
source venv/bin/activate
pip install -r requirements.txt

# Restart service
echo "🔁 Restarting Campfire service..."
sudo systemctl restart campfire.service


echo "✅ Update complete. Nova is up-to-date."
