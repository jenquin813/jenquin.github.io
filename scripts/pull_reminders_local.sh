#!/bin/bash
# pull_reminders_local.sh
# Converts LifeOrganizer CSV reminders to JSON for Jenquin-site calendar

set -e

# Paths
SOURCE_DIR="/Volumes/storage/projects/LifeOrganizer/life_organizer/modules/organized_reminders/data/nova_scheduling"
OUTPUT_FILE="/Volumes/storage/projects/Jenquin-site/data/reminders.local.json"
TEMP_FILE="/tmp/reminders_processing.json"

echo "🔄 Pulling reminders from LifeOrganizer..."

# Find the newest CSV file
NEWEST_CSV=$(find "$SOURCE_DIR" -name "*.csv" -type f | sort | tail -1)

if [ -z "$NEWEST_CSV" ]; then
    echo "❌ No CSV files found in $SOURCE_DIR"
    exit 1
fi

echo "📄 Processing: $(basename "$NEWEST_CSV")"

# Create temp directory for processing
mkdir -p "$(dirname "$TEMP_FILE")"

# Convert CSV to JSON using Python
export NEWEST_CSV
export TEMP_FILE
python3 << EOF
import csv
import json
import sys
from datetime import datetime
import os

source_file = os.environ['NEWEST_CSV']
temp_file = os.environ['TEMP_FILE']

items = []
count = 0
valid_count = 0

try:
    with open(source_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            count += 1
            
            # Skip completed items
            if row.get('completed', '').lower() in ['yes', 'true', '1']:
                continue
                
            # Skip items with invalid due dates
            due_str = row.get('due', '').strip()
            if not due_str or 'Error:' in due_str or due_str == 'No':
                continue
                
            try:
                # Parse the due date
                due_dt = datetime.strptime(due_str, '%Y-%m-%d %H:%M:%S')
                due_iso = due_dt.isoformat()
                
                # Convert to expected format
                item = {
                    'title': row.get('title', 'Untitled').strip(),
                    'dueISO': due_iso,
                    'list': row.get('list', 'Default').strip(),
                    'flagged': False,  # CSV doesn't have flagged field
                    'priority': 0,     # CSV doesn't have priority field
                    'id': row.get('id', '').strip()
                }
                
                items.append(item)
                valid_count += 1
                
            except ValueError:
                # Skip items with unparseable dates
                continue
    
    # Sort by due date
    items.sort(key=lambda x: x['dueISO'])
    
    # Create output structure
    output = {
        'items': items,
        'count': valid_count,
        'total_processed': count,
        'exported_at': datetime.now().isoformat(),
        'source_file': os.path.basename(source_file)
    }
    
    # Write to temp file
    with open(temp_file, 'w', encoding='utf-8') as outfile:
        json.dump(output, outfile, indent=2, ensure_ascii=False)
    
    print(f"✅ Processed {count} total rows, found {valid_count} valid scheduled reminders")

except Exception as e:
    print(f"❌ Error processing CSV: {e}")
    sys.exit(1)
EOF

# Check if Python processing succeeded
if [ $? -ne 0 ]; then
    echo "❌ Failed to process CSV data"
    exit 1
fi

# Ensure output directory exists
mkdir -p "$(dirname "$OUTPUT_FILE")"

# Move temp file to final location
mv "$TEMP_FILE" "$OUTPUT_FILE"

echo "📄 Output written to: $OUTPUT_FILE"
echo "🔍 Preview:"
head -20 "$OUTPUT_FILE"

echo ""
echo "✅ Reminders pull complete!"
echo "💡 Usage: python3 -m http.server 8080 from Jenquin-site root"
echo "🌐 Then open: http://localhost:8080/sandbox_calendar_agenda_card.html"