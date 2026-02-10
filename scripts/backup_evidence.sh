#!/bin/bash
# ============================================================
# نسخ احتياطي لمستودع الأدلة - منصة الشحانية الذكية
# Evidence Vault Backup Script for Al-Shahaniya Smart Platform (Linux)
# ============================================================

# مجلدات المصدر
SOURCE_DIR="/app/media/evidence_vault"

# مجلد النسخ الاحتياطي
BACKUP_ROOT="/var/backups/shaniya/evidence"
BACKUP_DAILY="${BACKUP_ROOT}/daily"

# إنشاء المجلدات إذا لم تكن موجودة
mkdir -p "${BACKUP_DAILY}"
mkdir -p "${BACKUP_ROOT}/logs"

# اسم الملف بالتاريخ
TIMESTAMP=$(date +"%Y-%m-%d_%H%M")
BACKUP_FILE="${BACKUP_DAILY}/evidence_vault_${TIMESTAMP}.tar.gz"
LOG_FILE="${BACKUP_ROOT}/logs/backup_$(date +"%Y-%m-%d").log"

echo "============================================================" >> "${LOG_FILE}"
echo "بدء النسخ الاحتياطي للأدلة: $(date)" >> "${LOG_FILE}"
echo "============================================================" >> "${LOG_FILE}"

# التحقق من وجود المجلد المصدر
if [ ! -d "${SOURCE_DIR}" ]; then
    echo "✗ المجلد المصدر غير موجود: ${SOURCE_DIR}" >> "${LOG_FILE}"
    echo "✗ المجلد المصدر غير موجود"
    exit 1
fi

# عد الملفات
echo "جاري فحص الملفات..."
echo "فحص الملفات..." >> "${LOG_FILE}"
FILE_COUNT=$(find "${SOURCE_DIR}" -type f | wc -l)
echo "عدد الملفات: ${FILE_COUNT}" >> "${LOG_FILE}"

# تنفيذ النسخ الاحتياطي
echo "جاري النسخ الاحتياطي لمستودع الأدلة..."
echo "جاري الضغط والنسخ..." >> "${LOG_FILE}"

tar -czf "${BACKUP_FILE}" -C "$(dirname ${SOURCE_DIR})" "$(basename ${SOURCE_DIR})"

if [ $? -eq 0 ]; then
    echo "✓ تم النسخ الاحتياطي بنجاح" >> "${LOG_FILE}"
    echo "✓ تم النسخ الاحتياطي بنجاح"
    
    # حساب حجم الملف
    SIZE=$(du -h "${BACKUP_FILE}" | cut -f1)
    echo "حجم الملف المضغوط: ${SIZE}" >> "${LOG_FILE}"
    echo "حجم الملف: ${SIZE}"
else
    echo "✗ فشل النسخ الاحتياطي" >> "${LOG_FILE}"
    echo "✗ فشل النسخ الاحتياطي"
    exit 1
fi

# حذف النسخ الاحتياطية الأقدم من 7 أيام
echo "جاري حذف النسخ القديمة..."
echo "حذف النسخ الأقدم من 7 أيام..." >> "${LOG_FILE}"
find "${BACKUP_DAILY}" -name "*.tar.gz" -type f -mtime +7 -delete

echo "============================================================" >> "${LOG_FILE}"
echo "انتهى النسخ الاحتياطي: $(date)" >> "${LOG_FILE}"
echo "============================================================" >> "${LOG_FILE}"
echo ""

echo "تم الانتهاء من النسخ الاحتياطي!"
