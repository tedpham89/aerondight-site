@echo off
REM Daily website data push - schedule every day ~8:15pm, after the research
REM repo's after-hour.bat (~7pm + ~35min) has finished writing the DBs.
REM Exports: current HMM/XGB regime (daily) + sector rotation weekly summary
REM (no-op unless a new completed week exists). Commits + pushes only when
REM something actually changed; Cloudflare Pages auto-deploys on push.
REM Safe to re-run anytime. The Saturday rotation task remains as backup.
REM
REM Register (one time):
REM   schtasks /create /tn "Aerondight site daily update" ^
REM     /tr "\"%~dp0update-site-daily.bat\"" /sc daily /st 20:15

setlocal
cd /d "%~dp0.."

python scripts\export_regime.py
if errorlevel 1 (
    echo [site-daily] regime export failed - continuing to rotation.
)
python scripts\export_rotation.py
if errorlevel 1 (
    echo [site-daily] rotation export failed.
)

git add src/data
git diff --cached --quiet
if not errorlevel 1 (
    echo [site-daily] no changes to publish - done.
    exit /b 0
)

git commit -m "Daily data update (regime / rotation)"
if errorlevel 1 (
    echo [site-daily] commit failed.
    exit /b 1
)
git push
if errorlevel 1 (
    echo [site-daily] push failed - commit is local, will retry tomorrow.
    exit /b 1
)
echo [site-daily] published.
endlocal
