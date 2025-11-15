#!/bin/bash
# pull_reminders_local.sh
# Modular data pipeline: Nova Scheduling CSV → Multiple JSON Views

set -e

# Paths
SOURCE_DIR="/Volumes/storage/projects/LifeOrganizer/life_organizer/modules/organized_reminders/data/nova_scheduling"
DATA_DIR="/Volumes/storage/projects/Jenquin-site/data"
SCRIPTS_DIR="/Volumes/storage/projects/Jenquin-site/scripts"

echo "🔄 Building reminders views from Nova Scheduling..."

# Find the newest CSV file
NEWEST_CSV=$(find "$SOURCE_DIR" -name "*.csv" -type f | sort | tail -1)

if [ -z "$NEWEST_CSV" ]; then
    echo "❌ No CSV files found in $SOURCE_DIR"
    exit 1
fi

echo "📄 Processing: $(basename "$NEWEST_CSV")"

# Ensure data directory exists
mkdir -p "$DATA_DIR"

# Copy source CSV for reference
cp "$NEWEST_CSV" "$DATA_DIR/nova_scheduling.csv"
echo "📋 Copied source CSV to data/nova_scheduling.csv"

# Build all views
echo ""
echo "🏗️ Building views..."

# Daily View (Today's Agenda Card)
python3 "$SCRIPTS_DIR/build_daily_view.py" "$NEWEST_CSV" "$DATA_DIR/daily.json"

# Backlog View (Overdue/Undated/Future)
python3 "$SCRIPTS_DIR/build_backlog_view.py" "$NEWEST_CSV" "$DATA_DIR/backlog.json"

# Projects View (Smart Planner Card)  
python3 "$SCRIPTS_DIR/build_project_view.py" "$NEWEST_CSV" "$DATA_DIR/projects.json"

# Week View (Next 7 Days)
python3 "$SCRIPTS_DIR/build_week_view.py" "$NEWEST_CSV" "$DATA_DIR/week.json"

echo ""
echo "📊 DATA FILES GENERATED:"
echo "├── nova_scheduling.csv  (source data)"
echo "├── daily.json          (today's agenda)" 
echo "├── backlog.json        (overdue/undated/future)"
echo "├── projects.json       (Smart Planner)"
echo "└── week.json           (next 7 days)"

echo ""
echo "✅ Pipeline complete!"
echo "💡 Usage: python3 -m http.server 8080 from Jenquin-site root"
echo "🌐 Jenquin App: http://localhost:8080"
echo "🧪 Calendar Test: http://localhost:8080/sandbox_calendar_loading_bar.html"