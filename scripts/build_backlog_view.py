#!/usr/bin/env python3
"""
build_backlog_view.py
Creates backlog.json for overdue and undated reminders.

Responsibility:
- Overdue reminders (due date < today)
- Undated reminders (no due date)
- Future reminders NOT scheduled today
- This is your "Everything else / Database view"
"""

import csv
import json
import sys
from datetime import datetime, date
from pathlib import Path

def build_backlog_view(source_csv, output_json):
    """Build backlog from Nova Scheduling CSV"""
    
    today = date.today()
    overdue_items = []
    undated_items = []
    future_items = []
    
    try:
        with open(source_csv, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                # Skip completed items
                if row.get('completed', '').lower() in ['yes', 'true', '1']:
                    continue
                    
                title = row.get('title', 'Untitled').strip()
                due_str = row.get('due', '').strip()
                
                # Create base item
                item = {
                    'title': title,
                    'list': row.get('list', 'Default').strip(),
                    'flagged': row.get('flagged', '').lower() in ['yes', 'true', '1'],
                    'priority': int(row.get('priority', 0) or 0),
                    'id': row.get('id', '').strip()
                }
                
                # Handle undated items
                if not due_str or 'Error:' in due_str or due_str == 'No':
                    item['category'] = 'undated'
                    undated_items.append(item)
                    continue
                    
                try:
                    due_dt = datetime.strptime(due_str, '%Y-%m-%d %H:%M:%S')
                    due_date = due_dt.date()
                    
                    item['dueISO'] = due_dt.isoformat()
                    item['due_date'] = due_date.isoformat()
                    
                    if due_date < today:
                        # Overdue
                        item['category'] = 'overdue'
                        item['days_overdue'] = (today - due_date).days
                        overdue_items.append(item)
                    elif due_date > today:
                        # Future (not today)
                        item['category'] = 'future'
                        item['days_until'] = (due_date - today).days
                        future_items.append(item)
                    # Skip today items - they go to daily view
                        
                except ValueError:
                    # Unparseable dates go to undated
                    item['category'] = 'undated'
                    undated_items.append(item)
    
        # Sort each category
        overdue_items.sort(key=lambda x: x.get('days_overdue', 0), reverse=True)  # Most overdue first
        future_items.sort(key=lambda x: x.get('dueISO', ''))  # Cronological
        undated_items.sort(key=lambda x: x['title'].lower())  # Alphabetical
        
        # Create output structure
        output = {
            'view': 'backlog',
            'date': today.isoformat(),
            'categories': {
                'overdue': {
                    'count': len(overdue_items),
                    'items': overdue_items
                },
                'undated': {
                    'count': len(undated_items), 
                    'items': undated_items
                },
                'future': {
                    'count': len(future_items),
                    'items': future_items
                }
            },
            'total_count': len(overdue_items) + len(undated_items) + len(future_items),
            'generated_at': datetime.now().isoformat()
        }
        
        # Write output
        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
            
        print(f"✅ Backlog view: {len(overdue_items)} overdue, {len(undated_items)} undated, {len(future_items)} future")
        return True
        
    except Exception as e:
        print(f"❌ Error building backlog view: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 build_backlog_view.py <source_csv> <output_json>")
        sys.exit(1)
        
    source_csv = sys.argv[1]
    output_json = sys.argv[2]
    
    success = build_backlog_view(source_csv, output_json)
    sys.exit(0 if success else 1)