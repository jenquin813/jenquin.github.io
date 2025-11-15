#!/usr/bin/env python3
"""
build_daily_view.py
Creates daily.json for today's agenda card.

Responsibility:
- Today only: reminders with due date == today
- Reminders with scheduled time today  
- Sorted by time
- NOTHING overdue, NOTHING future, NOTHING undated
- EXACT match with Apple Calendar "Today"
"""

import csv
import json
import sys
from datetime import datetime, date
from pathlib import Path

def build_daily_view(source_csv, output_json):
    """Build today's agenda from Nova Scheduling CSV"""
    
    today = date.today()
    today_items = []
    total_processed = 0
    valid_dates = 0
    error_dates = 0
    
    print(f"📁 Source CSV file: {source_csv}")
    print(f"🗓️ Looking for items due today: {today}")
    
    try:
        with open(source_csv, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                total_processed += 1
                
                # Skip completed items (CSV doesn't have completed field, so this won't match)
                # if row.get('completed', '').lower() in ['yes', 'true', '1']:
                #     continue
                    
                # Parse due date
                due_str = row.get('due', '').strip()
                if not due_str:
                    continue
                    
                if 'Error:' in due_str or due_str == 'No':
                    error_dates += 1
                    continue
                    
                try:
                    due_dt = datetime.strptime(due_str, '%Y-%m-%d %H:%M:%S')
                    due_date = due_dt.date()
                    valid_dates += 1
                    
                    # Debug: Show a few sample dates
                    if valid_dates <= 3:
                        print(f"   Sample item: '{row.get('title', '')}' due {due_date}")
                    
                    # Only include items due TODAY
                    if due_date == today:
                        print(f"   ✅ Found today item: '{row.get('title', '')}' at {due_dt.strftime('%H:%M')}")
                        item = {
                            'title': row.get('title', 'Untitled').strip(),
                            'dueISO': due_dt.isoformat(),
                            'time': due_dt.strftime('%H:%M'),
                            'list': row.get('list', 'Default').strip(),
                            'flagged': False,  # CSV doesn't have flagged field
                            'priority': 0,     # CSV doesn't have priority field
                            'id': row.get('id', '').strip()
                        }
                        today_items.append(item)
                        
                except ValueError as e:
                    error_dates += 1
                    continue
    
        # Sort by time
        today_items.sort(key=lambda x: x['dueISO'])
        
        print(f"\n📊 Processing Summary:")
        print(f"   Total rows: {total_processed}")
        print(f"   Valid dates: {valid_dates}")
        print(f"   Error dates: {error_dates}")
        print(f"   Items due today: {len(today_items)}")
        
        # Create output structure
        output = {
            'view': 'daily',
            'date': today.isoformat(),
            'count': len(today_items),
            'items': today_items,
            'stats': {
                'total_processed': total_processed,
                'valid_dates': valid_dates,
                'error_dates': error_dates
            },
            'generated_at': datetime.now().isoformat()
        }
        
        # Write output
        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
            
        print(f"✅ Daily view: {len(today_items)} items for {today}")
        return True
        
    except Exception as e:
        print(f"❌ Error building daily view: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 build_daily_view.py <source_csv> <output_json>")
        sys.exit(1)
        
    source_csv = sys.argv[1]
    output_json = sys.argv[2]
    
    success = build_daily_view(source_csv, output_json)
    sys.exit(0 if success else 1)