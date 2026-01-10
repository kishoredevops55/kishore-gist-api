@echo off
REM Quick Load Test using curl
REM Usage: quick-load-test.bat [requests] [endpoint]

setlocal enabledelayedexpansion

set REQUESTS=%1
if "%REQUESTS%"=="" set REQUESTS=50

set ENDPOINT=%2
if "%ENDPOINT%"=="" set ENDPOINT=/octocat

set HOST=gists.kishore.local
set SUCCESS=0
set FAILED=0

echo ============================================
echo Quick Load Test: %REQUESTS% requests to %ENDPOINT%
echo ============================================
echo.

for /L %%i in (1,1,%REQUESTS%) do (
    curl.exe -sk -o NUL -w "%%{http_code}" https://%HOST%%ENDPOINT% > temp_status.txt 2>nul
    set /p STATUS=<temp_status.txt
    if "!STATUS!"=="200" (
        set /a SUCCESS+=1
        <nul set /p =.
    ) else (
        set /a FAILED+=1
        <nul set /p =X
    )
)
del temp_status.txt 2>nul

echo.
echo.
echo ============================================
echo Results
echo ============================================
echo Total:     %REQUESTS%
echo Success:   %SUCCESS%
echo Failed:    %FAILED%
echo.

REM Show pod distribution
echo Pod Request Distribution:
kubectl logs -n production -l app=github-gists-api --tail=100 2>nul | findstr /C:"GET %ENDPOINT%" | find /c /v "" 
echo.
