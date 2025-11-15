-- AppleScript Bridge for Nova Refresh
-- This app will have Reminders permissions and can be called from cron/launchd

on run
	try
		set logPath to (path to home folder as string) & "refresh_nova.log"
		
		-- Log start
		set currentDate to (current date) as string
		do shell script "echo '" & currentDate & ": AppleScript bridge starting' >> " & quoted form of POSIX path of logPath
		
		-- Run the refresh script with explicit zsh
		do shell script "/bin/zsh /Volumes/storage/projects/Jenquin-site/refresh_nova.sh"
		
		-- Log success
		set currentDate to (current date) as string
		do shell script "echo '" & currentDate & ": AppleScript bridge finished OK' >> " & quoted form of POSIX path of logPath
		
		return "Nova refresh completed successfully"
		
	on error errMsg
		-- Log error
		set currentDate to (current date) as string
		set logPath to (path to home folder as string) & "refresh_nova.log"
		do shell script "echo '" & currentDate & ": AppleScript bridge ERROR: " & errMsg & "' >> " & quoted form of POSIX path of logPath
		
		return "Nova refresh failed: " & errMsg
	end try
end run