@echo off
REM ============================================================
REM نسخ احتياطي لقاعدة بيانات منصة الشحانية الذكية
REM Database Backup Script for Al-Shahaniya Smart Platform
REM ============================================================

setlocal enabledelayedexpansion

REM إعدادات قاعدة البيانات
set DB_NAME=shaniya
set DB_USER=app_admin
set DB_HOST=localhost
set DB_PORT=5434

REM مجلد النسخ الاحتياطي
set BACKUP_ROOT=D:\SULTAN_HAGRY\backups\database
set BACKUP_DAILY=%BACKUP_ROOT%\daily
set BACKUP_WEEKLY=%BACKUP_ROOT%\weekly
set BACKUP_MONTHLY=%BACKUP_ROOT%\monthly

REM إنشاء المجلدات إذا لم تكن موجودة
if not exist "%BACKUP_DAILY%" mkdir "%BACKUP_DAILY%"
if not exist "%BACKUP_WEEKLY%" mkdir "%BACKUP_WEEKLY%"
if not exist "%BACKUP_ROOT%\logs" mkdir "%BACKUP_ROOT%\logs"

REM اسم الملف بالتاريخ
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c-%%a-%%b)
for /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set mytime=%%a%%b)
set TIMESTAMP=%mydate%_%mytime%
set BACKUP_FILE=%BACKUP_DAILY%\%DB_NAME%_%TIMESTAMP%.sql

REM سجل العمليات
set LOG_FILE=%BACKUP_ROOT%\logs\backup_%mydate%.log

echo ============================================================ >> "%LOG_FILE%"
echo بدء النسخ الاحتياطي: %date% %time% >> "%LOG_FILE%"
echo ============================================================ >> "%LOG_FILE%"

REM تنفيذ النسخ الاحتياطي
echo جاري النسخ الاحتياطي لقاعدة البيانات...
echo جاري النسخ الاحتياطي... >> "%LOG_FILE%"

docker exec -t postgres pg_dump -U %DB_USER% -h localhost -p %DB_PORT% %DB_NAME% > "%BACKUP_FILE%"

if %ERRORLEVEL% EQU 0 (
    echo ✓ تم النسخ الاحتياطي بنجاح >> "%LOG_FILE%"
    echo ✓ تم النسخ الاحتياطي بنجاح
    
    REM ضغط الملف
    echo جاري ضغط الملف...
    echo جاري الضغط... >> "%LOG_FILE%"
    powershell -command "Compress-Archive -Path '%BACKUP_FILE%' -DestinationPath '%BACKUP_FILE%.zip' -Force"
    
    if %ERRORLEVEL% EQU 0 (
        echo ✓ تم الضغط بنجاح >> "%LOG_FILE%"
        del "%BACKUP_FILE%"
        
        REM حساب حجم الملف
        for %%A in ("%BACKUP_FILE%.zip") do set SIZE=%%~zA
        set /a SIZE_MB=!SIZE! / 1048576
        echo حجم الملف: !SIZE_MB! MB >> "%LOG_FILE%"
    ) else (
        echo ✗ فشل الضغط >> "%LOG_FILE%"
    )
) else (
    echo ✗ فشل النسخ الاحتياطي >> "%LOG_FILE%"
    echo ✗ فشل النسخ الاحتياطي
    exit /b 1
)

REM حذف النسخ الاحتياطية الأقدم من 7 أيام
echo جاري حذف النسخ القديمة...
echo حذف النسخ الأقدم من 7 أيام... >> "%LOG_FILE%"
forfiles /P "%BACKUP_DAILY%" /M *.zip /D -7 /C "cmd /c del @path" 2>nul

echo ============================================================ >> "%LOG_FILE%"
echo انتهى النسخ الاحتياطي: %date% %time% >> "%LOG_FILE%"
echo ============================================================ >> "%LOG_FILE%"
echo.

echo تم الانتهاء من النسخ الاحتياطي!
endlocal
