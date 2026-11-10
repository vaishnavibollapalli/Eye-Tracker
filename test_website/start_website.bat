@echo off
rem Double-click to start the Poster Gaze Explorer and open it in the browser.
rem Keep this window open while presenting; close it (or press Ctrl+C) to stop.
title Poster Gaze Explorer
cd /d "%~dp0.."
python test_website\app.py --open
pause
