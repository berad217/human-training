@echo off
REM ---------------------------------------------------------------------------
REM Update the INSTALLED human-training plugin to the latest version on GitHub.
REM
REM Why two commands: Claude Code checks a LOCAL catalog cache, not GitHub
REM directly. Line 1 force-refreshes that cache (the step autoUpdate keeps
REM skipping); line 2 installs whatever the refreshed cache now reports.
REM
REM Run this on any machine after pushing new commits. It pulls from GitHub,
REM so it does NOT need this repo to be cloned or up to date locally.
REM ---------------------------------------------------------------------------

echo [1/2] Refreshing marketplace catalog from GitHub...
call claude plugin marketplace update human-training

echo.
echo [2/2] Installing latest plugin version...
call claude plugin update human-training@human-training

echo.
echo Done. Now FULLY quit and relaunch Claude Code to load it
echo (a new thread / resumed session is NOT enough).
pause
