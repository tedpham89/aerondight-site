@echo off
REM Weekly sector rotation website update - schedule Saturdays (e.g. 9:00am).
REM Exports the latest official weekly rotation summary from the research
REM repo's rotation_paper.db into src/data/rotation/, then commits + pushes.
REM Cloudflare Pages auto-deploys on push. Safe to re-run: the exporter only
REM writes missing weeks, and nothing is committed when there is no change.
REM
REM Register the scheduled task (one time, from this folder):
REM   schtasks /create /tn "Aerondight rotation site update" ^
REM     /tr "\"%~dp0update-rotation.bat\"" /sc weekly /d SAT /st 09:00

setlocal
cd /d "%~dp0.."

python scripts\export_rotation.py
if errorlevel 1 (
    echo [rotation-site] export failed - aborting, nothing pushed.
    exit /b 1
)

git add src/data/rotation
git diff --cached --quiet
if not errorlevel 1 (
    echo [rotation-site] no new week to publish - done.
    exit /b 0
)

for /f %%i in ('git diff --cached --name-only') do set "NEWFILE=%%i"
git commit -m "Weekly sector rotation update"
if errorlevel 1 (
    echo [rotation-site] commit failed.
    exit /b 1
)
git push
if errorlevel 1 (
    echo [rotation-site] push failed - commit is local, will retry next week.
    exit /b 1
)
echo [rotation-site] published %NEWFILE%.
endlocal
