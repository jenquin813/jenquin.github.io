#!/usr/bin/env python3
"""
build_project_view.py
Creates projects.json for the Smart Planner card.

Responsibility:
- Project tasks
- Roadmap phases  
- Anything tagged "project" in Nova Scheduling
- Future AI logic can pick which task is next
"""

import csv
import json
import sys
import re
from datetime import datetime, date
from pathlib import Path

def is_project_item(title, list_name):
    """Determine if an item is project-related"""
    title_lower = title.lower()
    list_lower = list_name.lower()
    
    # Check for project keywords
    project_keywords = ['project', 'phase', 'milestone', 'roadmap', 'epic', 'feature']
    
    # Check title for project indicators
    if any(keyword in title_lower for keyword in project_keywords):
        return True
        
    # Check for project-style formatting (Project — Name, Phase: Name)
    if re.match(r'^project\s*[—-]\s*', title_lower):
        return True
    if re.match(r'^phase\s*:\s*', title_lower):
        return True
        
    # Check list names that indicate projects
    if 'project' in list_lower or 'roadmap' in list_lower:
        return True
        
    return False

def extract_project_info(title):
    """Extract project and phase info from title"""
    # Match "Project — Name" format
    project_match = re.match(r'^project\s*[—-]\s*(.+)', title.strip(), re.IGNORECASE)
    if project_match:
        return {
            'type': 'project',
            'project_name': project_match.group(1).strip(),
            'phase': None
        }
    
    # Match "Phase: Description" format  
    phase_match = re.match(r'^phase\s*:\s*(.+)', title.strip(), re.IGNORECASE)
    if phase_match:
        return {
            'type': 'phase',
            'project_name': None,
            'phase': phase_match.group(1).strip()
        }
    
    # Default to task
    return {
        'type': 'task',
        'project_name': None,
        'phase': None
    }

def build_project_view(source_csv, output_json):
    """Build projects view from Nova Scheduling CSV"""
    
    today = date.today()
    project_items = []
    
    try:
        with open(source_csv, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                # Skip completed items
                if row.get('completed', '').lower() in ['yes', 'true', '1']:
                    continue
                    
                title = row.get('title', 'Untitled').strip()
                list_name = row.get('list', 'Default').strip()
                
                # Only include project-related items
                if not is_project_item(title, list_name):
                    continue
                
                # Parse due date if exists
                due_str = row.get('due', '').strip()
                due_dt = None
                due_date = None
                
                if due_str and 'Error:' not in due_str and due_str != 'No':
                    try:
                        due_dt = datetime.strptime(due_str, '%Y-%m-%d %H:%M:%S')
                        due_date = due_dt.date()
                    except ValueError:
                        pass
                
                # Extract project structure
                project_info = extract_project_info(title)
                
                item = {
                    'title': title,
                    'type': project_info['type'],
                    'project_name': project_info['project_name'],
                    'phase': project_info['phase'],
                    'list': list_name,
                    'flagged': row.get('flagged', '').lower() in ['yes', 'true', '1'],
                    'priority': int(row.get('priority', 0) or 0),
                    'id': row.get('id', '').strip()
                }
                
                if due_dt:
                    item['dueISO'] = due_dt.isoformat()
                    item['due_date'] = due_date.isoformat()
                    item['status'] = 'overdue' if due_date < today else 'scheduled'
                else:
                    item['status'] = 'backlog'
                
                project_items.append(item)
    
        # Group by project name or list
        projects = {}
        standalone_items = []
        
        for item in project_items:
            project_key = item['project_name'] or item['list']
            
            if project_key not in projects:
                projects[project_key] = {
                    'name': project_key,
                    'items': [],
                    'phases': {},
                    'total_items': 0
                }
            
            projects[project_key]['items'].append(item)
            projects[project_key]['total_items'] += 1
            
            # Group phases within projects
            if item['phase']:
                phase_key = item['phase']
                if phase_key not in projects[project_key]['phases']:
                    projects[project_key]['phases'][phase_key] = []
                projects[project_key]['phases'][phase_key].append(item)
        
        # Sort projects and items
        sorted_projects = []
        for project_name, project_data in projects.items():
            # Sort items within project by priority, then due date
            project_data['items'].sort(key=lambda x: (
                -x['priority'],  # Higher priority first
                x.get('dueISO', 'z'),  # Earlier due dates first
                x['title']
            ))
            sorted_projects.append(project_data)
        
        # Sort projects by total priority
        sorted_projects.sort(key=lambda x: sum(item['priority'] for item in x['items']), reverse=True)
        
        # Create output structure
        output = {
            'view': 'projects',
            'date': today.isoformat(),
            'projects': sorted_projects,
            'total_projects': len(sorted_projects),
            'total_items': len(project_items),
            'generated_at': datetime.now().isoformat()
        }
        
        # Write output
        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
            
        print(f"✅ Projects view: {len(sorted_projects)} projects, {len(project_items)} total items")
        return True
        
    except Exception as e:
        print(f"❌ Error building projects view: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 build_project_view.py <source_csv> <output_json>")
        sys.exit(1)
        
    source_csv = sys.argv[1]
    output_json = sys.argv[2]
    
    success = build_project_view(source_csv, output_json)
    sys.exit(0 if success else 1)