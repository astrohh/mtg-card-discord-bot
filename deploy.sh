#!/bin/bash

echo "📦 Pulling latest changes (if repo is clean)..."
git pull

echo "🔁 Restarting mtg-bot systemd service..."
sudo systemctl restart mtg-bot.service

echo "✅ Bot restarted. Showing logs (Ctrl+C to stop)..."
sudo journalctl -u mtg-bot.service -f
echo "🚀 Deployment complete!"