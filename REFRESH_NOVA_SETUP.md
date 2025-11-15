# Nova Scheduling Pipeline Fix

## Problem Solved
The data pipeline worked when run directly from Mac Terminal but failed silently when triggered remotely via Shortcuts/phone, causing the dashboard to serve stale data.

## Root Cause
1. **Environment Issues**: `source venv/bin/activate` doesn't work reliably in Shortcuts environment
2. **Permission Issues**: macOS Shortcuts may lack access to `/Volumes/storage/` paths  
3. **Silent Failures**: Original script continued running even when steps failed

## Solution: Bulletproof Script

Created [`/Volumes/storage/projects/Jenquin-site/refresh_nova.sh`](refresh_nova.sh:1):

### Key Improvements
- **Explicit Python Path**: Uses `$PROJECT_DIR/venv/bin/python` instead of `source` + `python`
- **Error Handling**: `set -e` stops execution on first failure
- **Explicit Checks**: `cd "$DIR" || { echo "Failed"; exit 1; }` pattern  
- **Debug Logging**: All operations logged to `~/refresh_nova.log`
- **Shell Specification**: Uses `#!/bin/zsh` (Mac's default shell)

## Setup Instructions

### 1. Test the Script
```bash
cd /Volumes/storage/projects/Jenquin-site
./refresh_nova.sh
```

Check the log:
```bash
cat ~/refresh_nova.log
```

### 2. Create macOS Shortcut (on Mac Mini)
1. Open **Shortcuts** app on Mac
2. Click **"+" to create new shortcut**
3. Name it **"Refresh Nova"**
4. Add action: **"Run Shell Script"**
5. Set script to:
   ```bash
   /Volumes/storage/projects/Jenquin-site/refresh_nova.sh
   ```
6. **Save the shortcut**

### 3. Test macOS Shortcut
1. Run the **"Refresh Nova"** shortcut on Mac
2. Verify agenda data updates in the dashboard
3. Check `~/refresh_nova.log` for any issues

### 4. Setup Phone Integration  
1. On your **iPhone**, open Shortcuts app
2. Create new shortcut called **"Update Nova"**
3. Add action: **"Run Shortcut on Mac"** 
4. Select: **"Refresh Nova"** (the Mac shortcut)
5. Test by saying **"Hey Siri, Update Nova"**

## Verification

### Success Indicators:
- ✅ `~/refresh_nova.log` shows start/finish timestamps
- ✅ Dashboard loads fresh agenda items
- ✅ Works identically from Terminal and Shortcuts

### Troubleshooting:
- **No log file**: Script never started (permission/path issue)
- **Log shows "Failed to cd"**: /Volumes/storage permission problem 
- **Log stops mid-execution**: Python environment issue
- **Data doesn't update**: Check [`data/daily.json`](data/daily.json:1) timestamp

## Data Flow
```
Nova Reminders → export → dedupe → tag → nova_scheduling.csv → JSON views → Dashboard
```

## Files Updated:
- [`refresh_nova.sh`](refresh_nova.sh:1) - Main bulletproof script
- [`scripts/pull_reminders_local.sh`](scripts/pull_reminders_local.sh:1) - Modular JSON builder (unchanged)
- `~/refresh_nova.log` - Debug log for remote execution

## Next Steps:
1. Save this Shortcut setup for voice-activated **"Update Nova"** commands
2. Monitor `~/refresh_nova.log` for any remote execution issues  
3. The dashboard will now stay current with live Nova Scheduling data!