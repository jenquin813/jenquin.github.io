#!/bin/zsh
set -e  # stop on first error

PROJECT_DIR="/Volumes/storage/projects/LifeOrganizer"
SITE_DIR="/Volumes/storage/projects/Jenquin-site"

# Log for debugging
echo "$(date): refresh_nova starting" >> "$HOME/refresh_nova.log"

cd "$PROJECT_DIR" || { echo "Failed to cd to $PROJECT_DIR" >> "$HOME/refresh_nova.log"; exit 1; }

# Sanity check: can we see the project?
ls "$PROJECT_DIR" >> "$HOME/refresh_nova.log" 2>&1

# Use venv's python explicitly (don't rely on 'source' + bare 'python')
VENV_PY="$PROJECT_DIR/venv/bin/python"

$VENV_PY -m life_organizer.modules.organized_reminders.scripts.export_reminders
$VENV_PY -m life_organizer.modules.organized_reminders.scripts.deduplicate_reminders
$VENV_PY -m life_organizer.modules.organized_reminders.scripts.reminder_tagger --commit

cd "$SITE_DIR" || { echo "Failed to cd to $SITE_DIR" >> "$HOME/refresh_nova.log"; exit 1; }

./scripts/pull_reminders_local.sh

echo "$(date): refresh_nova finished OK" >> "$HOME/refresh_nova.log"