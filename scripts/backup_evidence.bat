@echo off
REM ============================================================
REM نسخ احتياطي لمستودع الأدلة - منصة الشحانية الذكية
REM Evidence Vault Backup Script for Al-Shahaniya Smart Platform
REM ============================================================

setlocal enabledelayedexpansion

REM مجلدات المصدر
set SOURCE_DIR=D:\SULTAN_HAGRY\media\evidence_vault
set MEDIA_DIR=D:\SULTAN_HAGRY\media

REM مجلد النسخ الاحتياطي
set BACKUP_ROOT=D:\SULTAN_HAGRY\backups\evidence
set BACKUP_DAILY=%BACKUP_ROOT%\daily

REM إنشاء المجلدات إذا لم تكن موجودة
if not exist "%BACKUP_DAILY%" mkdir "%BACKUP_DAILY%"
if not exist "%BACKUP_ROOT%\logs" mkdir "%BACKUP_ROOT%\logs"

REM اسم الملف بالتاريخ
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c-%%a-%%b)
for /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set mytime=%%a%%b)
set TIMESTAMP=%mydate%_%mytime%
set BACKUP_FILE=%BACKUP_DAILY%\evidence_vault_%TIMESTAMP%.zip

REM سجل العمليات
set LOG_FILE=%BACKUP_ROOT%\logs\backup_%mydate%.log

echo ============================================================ >> "%LOG_FILE%"
echo بدء النسخ الاحتياطي للأدلة: %date% %time% >> "%LOG_FILE%"
echo ============================================================ >> "%LOG_FILE%"

REM التحقق من وجود المجلد المصدر
if not exist "%SOURCE_DIR%" (
    echo ✗ المجلد المصدر غير موجود: %SOURCE_DIR% >> "%LOG_FILE%"
    echo ✗ المجلد المصدر غير موجود
    exit /b 1
)

REM عد الملفات
echo جاري فحص الملفات...
echo فحص الملفات... >> "%LOG_FILE%"
set FILE_COUNT=0
for /r "%SOURCE_DIR%" %%f in (*) do set /a FILE_COUNT+=1
echo عدد الملفات: !FILE_COUNT! >> "%LOG_FILE%"

REM تنفيذ النسخ الاحتياطي
echo جاري النسخ الاحتياطي لمستودع الأدلة...
echo جاري الضغط والنسخ... >> "%LOG_FILE%"

powershell -command "Compress-Archive -Path '%SOURCE_DIR%\*' -DestinationPath '%BACKUP_FILE%' -CompressionLevel Optimal -Force"

if %ERRORLEVEL% EQU 0 (
    echo ✓ تم النسخ الاحتياطي بنجاح >> "%LOG_FILE%"
    echo ✓ تم النسخ الاحتياطي بنجاح
    
    REM حساب حجم الملف
    for %%A in ("%BACKUP_FILE%") do set SIZE=%%~zA
    set /a SIZE_MB=!SIZE! / 1048576
    echo حجم الملف المضغوط: !SIZE_MB! MB >> "%LOG_FILE%"
    echo حجم الملف: !SIZE_MB! MB
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
