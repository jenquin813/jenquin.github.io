#!/usr/bin/env python3
"""
Patch for reminder_tagger.py to auto-cleanup synthetic instances 
when original reminders are deleted.
"""

def clean_synthetic_instances_patch(all_reminders, current_export_ids):
    """
    Remove synthetic instances whose original reminders no longer exist
    in the current Apple Reminders export.
    
    Args:
        all_reminders: List of all reminders (including synthetic)
        current_export_ids: Set of reminder IDs from current export
    
    Returns:
        Cleaned list of reminders with orphaned synthetics removed
    """
    cleaned = []
    removed_count = 0
    
    for reminder in all_reminders:
        # Check if this is a synthetic instance
        if reminder.get('synthetic'):
            # Extract original ID (remove _synthetic_YYYYMMDD suffix)
            original_id = reminder.get('id', '').split('_synthetic_')[0]
            
            # Only keep synthetic if original still exists in current export
            if original_id in current_export_ids:
                cleaned.append(reminder)
            else:
                removed_count += 1
                print(f"🧹 Cleaned orphaned synthetic: {reminder.get('title', 'Unknown')}")
        else:
            # Keep all non-synthetic reminders
            cleaned.append(reminder)
    
    if removed_count > 0:
        print(f"🧹 Auto-cleanup: Removed {removed_count} orphaned synthetic instances")
    
    return cleaned

def enhanced_recurrence_generator(reminders, current_export_ids):
    """
    Enhanced recurrence generator with automatic synthetic cleanup.
    
    Args:
        reminders: List of deduplicated reminders
        current_export_ids: Set of reminder IDs from current export
    
    Returns:
        List with synthetic instances added and orphans cleaned
    """
    import datetime
    
    # First, clean any existing synthetic instances whose originals are deleted
    cleaned_reminders = clean_synthetic_instances_patch(reminders, current_export_ids)
    
    today = datetime.datetime.now().date()
    output = list(cleaned_reminders)  # Start with cleaned list
    synthetic_count = 0
    
    # Index to avoid duplicate same-day instances
    instance_index = {}
    for r in cleaned_reminders:
        if r.get("due"):
            try:
                due_date = datetime.datetime.strptime(r["due"][:10], "%Y-%m-%d").date()
                instance_index[(r["title"], due_date)] = True
            except:
                pass

    # Generate synthetic instances for current valid reminders only
    for r in cleaned_reminders:
        # Skip if reminder doesn't exist in current export
        if not r.get('synthetic') and r.get('id') not in current_export_ids:
            continue
            
        # Skip if already synthetic
        if r.get('synthetic'):
            continue
            
        # Check for recurrence patterns
        recurrence = r.get("recurrence", "").lower() if r.get("recurrence") else ""
        
        # Simple daily pattern detection
        is_likely_daily = False
        title = r.get("title", "").lower()
        daily_keywords = ["daily", "every day", "water", "feed", "walk", "exercise"]
        if any(keyword in title for keyword in daily_keywords):
            is_likely_daily = True

        # Skip if already have instance for today
        if (r["title"], today) in instance_index:
            continue

        # Generate daily recurrence instance
        if recurrence == "daily" or is_likely_daily:
            synthetic = generate_today_instance(r, today)
            output.append(synthetic)
            instance_index[(r["title"], today)] = True
            synthetic_count += 1

    print(f"Recurrence generator: Created {synthetic_count} synthetic instances for today")
    return output

def generate_today_instance(reminder, today):
    """
    Creates a synthetic 'today' instance of a repeating reminder.
    Does NOT alter the original reminder.
    """
    # Extract time from original due date, default to 09:00:00 if parsing fails
    original_time = "09:00:00"
    if reminder.get("due"):
        try:
            original_time = reminder["due"][11:]  # Extract time part
            if not original_time:
                original_time = "09:00:00"
        except:
            pass
    
    return {
        **reminder,  # copy all fields
        "due": today.strftime("%Y-%m-%d ") + original_time,
        "synthetic": True,
        "id": reminder.get("id", "") + "_synthetic_" + today.strftime("%Y%m%d")  # unique synthetic ID
    }

# Instructions for patching:
"""
In reminder_tagger.py, replace the recurrence_generator function call with:

# Before tagging, get current export IDs
current_export_ids = set(r.get('id', '') for r in deduplicated_reminders if r.get('id'))

# Enhanced recurrence generation with cleanup
tagged_reminders = enhanced_recurrence_generator(tagged_reminders, current_export_ids)
"""