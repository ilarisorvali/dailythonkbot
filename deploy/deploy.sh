#!/usr/bin/env bash
set -euo pipefail

QUADLET_DIR="$HOME/.config/containers/systemd"
SYSTEMD_USER_DIR="$HOME/.config/systemd/user"

mkdir -p "$QUADLET_DIR"
mkdir -p "$SYSTEMD_USER_DIR"

# Install Quadlet container definitions
install -m 644 ajatus.container "$QUADLET_DIR/"
install -m 644 christmas_calendar.container "$QUADLET_DIR/"
install -m 644 recipes.container "$QUADLET_DIR/"

# Install systemd user timers
install -m 644 ajatus.timer "$SYSTEMD_USER_DIR/"
install -m 644 christmas_calendar.timer "$SYSTEMD_USER_DIR/"
install -m 644 recipes.timer "$SYSTEMD_USER_DIR/"

# Reload user units
systemctl --user daemon-reload

# Enable and start timers
systemctl --user enable --now ajatus.timer
systemctl --user enable --now christmas_calendar.timer
systemctl --user enable --now recipes.timer

echo "Deployment complete."
echo
echo "Installed containers to: $QUADLET_DIR"
echo "Installed timers to:     $SYSTEMD_USER_DIR"
