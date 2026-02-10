#!/bin/bash
# ============================================================
# نسخ احتياطي لقاعدة بيانات منصة الشحانية الذكية
# Database Backup Script for Al-Shahaniya Smart Platform (Linux)
# ============================================================

# إعدادات قاعدة البيانات
DB_NAME="shaniya"
DB_USER="app_admin"
DB_HOST="localhost"
DB_PORT="5434"
DB_PASSWORD="${POSTGRES_PASSWORD}"

# مجلد النسخ الاحتياطي
BACKUP_ROOT="/var/backups/shaniya/database"
BACKUP_DAILY="${BACKUP_ROOT}/daily"
BACKUP_WEEKLY="${BACKUP_ROOT}/weekly"
BACKUP_MONTHLY="${BACKUP_ROOT}/monthly"

# إنشاء المجلدات إذا لم تكن موجودة
mkdir -p "${BACKUP_DAILY}"
mkdir -p "${BACKUP_WEEKLY}"
mkdir -p "${BACKUP_MONTHLY}"
mkdir -p "${BACKUP_ROOT}/logs"

# اسم الملف بالتاريخ
TIMESTAMP=$(date +"%Y-%m-%d_%H%M")
BACKUP_FILE="${BACKUP_DAILY}/${DB_NAME}_${TIMESTAMP}.sql"
LOG_FILE="${BACKUP_ROOT}/logs/backup_$(date +"%Y-%m-%d").log"

echo "============================================================" >> "${LOG_FILE}"
echo "بدء النسخ الاحتياطي: $(date)" >> "${LOG_FILE}"
echo "============================================================" >> "${LOG_FILE}"

# تنفيذ النسخ الاحتياطي
echo "جاري النسخ الاحتياطي لقاعدة البيانات..."
echo "جاري النسخ الاحتياطي..." >> "${LOG_FILE}"

PGPASSWORD="${DB_PASSWORD}" pg_dump -U "${DB_USER}" -h "${DB_HOST}" -p "${DB_PORT}" "${DB_NAME}" > "${BACKUP_FILE}"

if [ $? -eq 0 ]; then
    echo "✓ تم النسخ الاحتياطي بنجاح" >> "${LOG_FILE}"
    echo "✓ تم النسخ الاحتياطي بنجاح"
    
    # ضغط الملف
    echo "جاري ضغط الملف..."
    echo "جاري الضغط..." >> "${LOG_FILE}"
    gzip "${BACKUP_FILE}"
    
    if [ $? -eq 0 ]; then
        echo "✓ تم الضغط بنجاح" >> "${LOG_FILE}"
        
        # حساب حجم الملف
        SIZE=$(du -h "${BACKUP_FILE}.gz" | cut -f1)
        echo "حجم الملف: ${SIZE}" >> "${LOG_FILE}"
    else
        echo "✗ فشل الضغط" >> "${LOG_FILE}"
    fi
else
    echo "✗ فشل النسخ الاحتياطي" >> "${LOG_FILE}"
    echo "✗ فشل النسخ الاحتياطي"
    exit 1
fi

# حذف النسخ الاحتياطية الأقدم من 7 أيام
echo "جاري حذف النسخ القديمة..."
echo "حذف النسخ الأقدم من 7 أيام..." >> "${LOG_FILE}"
find "${BACKUP_DAILY}" -name "*.sql.gz" -type f -mtime +7 -delete

# نسخ أسبوعي (كل يوم أحد)
if [ $(date +%u) -eq 7 ]; then
    echo "إنشاء نسخة أسبوعية..." >> "${LOG_FILE}"
    cp "${BACKUP_FILE}.gz" "${BACKUP_WEEKLY}/${DB_NAME}_weekly_${TIMESTAMP}.sql.gz"
fi

# نسخ شهري (أول يوم من الشهر)
if [ $(date +%d) -eq 01 ]; then
    echo "إنشاء نسخة شهرية..." >> "${LOG_FILE}"
    cp "${BACKUP_FILE}.gz" "${BACKUP_MONTHLY}/${DB_NAME}_monthly_${TIMESTAMP}.sql.gz"
fi

echo "============================================================" >> "${LOG_FILE}"
echo "انتهى النسخ الاحتياطي: $(date)" >> "${LOG_FILE}"
echo "============================================================" >> "${LOG_FILE}"
echo ""

echo "تم الانتهاء من النسخ الاحتياطي!"
