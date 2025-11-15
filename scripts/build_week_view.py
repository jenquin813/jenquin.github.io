#!/usr/bin/env python3
"""
build_week_view.py
Creates week.json for the next 7 days schedule.

Responsibility:
- Reminders scheduled for the next 7 days
- Sorted by day/time
- Eventually: plus zone logic, energy logic, etc
"""

import csv
import json
import sys
from datetime import datetime, date, timedelta
from pathlib import Path

def build_week_view(source_csv, output_json):
    """Build week view from Nova Scheduling CSV"""
    
    today = date.today()
    week_end = today + timedelta(days=7)
    week_items = []
    
    try:
        with open(source_csv, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                # Skip completed items
                if row.get('completed', '').lower() in ['yes', 'true', '1']:
                    continue
                    
                # Parse due date
                due_str = row.get('due', '').strip()
                if not due_str or 'Error:' in due_str or due_str == 'No':
                    continue
                    
                try:
                    due_dt = datetime.strptime(due_str, '%Y-%m-%d %H:%M:%S')
                    due_date = due_dt.date()
                    
                    # Only include items in the next 7 days (including today)
                    if today <= due_date <= week_end:
                        day_name = due_date.strftime('%A')
                        days_from_now = (due_date - today).days
                        
                        item = {
                            'title': row.get('title', 'Untitled').strip(),
                            'dueISO': due_dt.isoformat(),
                            'due_date': due_date.isoformat(),
                            'time': due_dt.strftime('%H:%M'),
                            'day_name': day_name,
                            'days_from_now': days_from_now,
                            'list': row.get('list', 'Default').strip(),
                            'flagged': row.get('flagged', '').lower() in ['yes', 'true', '1'],
                            'priority': int(row.get('priority', 0) or 0),
                            'id': row.get('id', '').strip()
                        }
                        
                        # Add relative labels
                        if days_from_now == 0:
                            item['relative_day'] = 'Today'
                        elif days_from_now == 1:
                            item['relative_day'] = 'Tomorrow'
                        else:
                            item['relative_day'] = f"In {days_from_now} days"
                            
                        week_items.append(item)
                        
                except ValueError:
                    # Skip unparseable dates
                    continue
    
        # Sort by date, then time
        week_items.sort(key=lambda x: x['dueISO'])
        
        # Group by day
        days = {}
        for item in week_items:
            day_key = item['due_date']
            if day_key not in days:
                days[day_key] = {
                    'date': day_key,
                    'day_name': item['day_name'],
                    'relative_day': item['relative_day'],
                    'days_from_now': item['days_from_now'],
                    'items': []
                }
            days[day_key]['items'].append(item)
        
        # Convert to sorted list
        sorted_days = sorted(days.values(), key=lambda x: x['date'])
        
        # Add day summaries
        for day in sorted_days:
            day['item_count'] = len(day['items'])
            day['priority_items'] = len([item for item in day['items'] if item['priority'] > 0])
            day['flagged_items'] = len([item for item in day['items'] if item['flagged']])
        
        # Create output structure
        output = {
            'view': 'week',
            'start_date': today.isoformat(),
            'end_date': week_end.isoformat(),
            'days': sorted_days,
            'total_days': len(sorted_days),
            'total_items': len(week_items),
            'summary': {
                'total_items': len(week_items),
                'priority_items': len([item for item in week_items if item['priority'] > 0]),
                'flagged_items': len([item for item in week_items if item['flagged']]),
                'items_by_day': {day['relative_day']: day['item_count'] for day in sorted_days}
            },
            'generated_at': datetime.now().isoformat()
        }
        
        # Write output
        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
            
        print(f"✅ Week view: {len(week_items)} items across {len(sorted_days)} days")
        return True
        
    except Exception as e:
        print(f"❌ Error building week view: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 build_week_view.py <source_csv> <output_json>")
        sys.exit(1)
        
    source_csv = sys.argv[1]
    output_json = sys.argv[2]
    
    success = build_week_view(source_csv, output_json)
    sys.exit(0 if success else 1)