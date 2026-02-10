# دليل النسخ الاحتياطي الآلي

## نظرة عامة

تم إنشاء نظام نسخ احتياطي آلي شامل للمنصة يتضمن:

- نسخ احتياطي يومي لقاعدة البيانات PostgreSQL
- نسخ احتياطي يومي لمستودع الأدلة
- استراتيجية احتفاظ تلقائية

---

## السكريبتات المتوفرة

### Windows

- `scripts/backup_database.bat` - نسخ قاعدة البيانات
- `scripts/backup_evidence.bat` - نسخ مستودع الأدلة

### Linux

- `scripts/backup_database.sh` - نسخ قاعدة البيانات
- `scripts/backup_evidence.sh` - نسخ مستودع الأدلة

---

## الإعداد الأولي

### 1. إنشاء مجلدات النسخ الاحتياطي

```bash
# Windows
mkdir D:\SULTAN_HAGRY\backups\database\daily
mkdir D:\SULTAN_HAGRY\backups\database\weekly
mkdir D:\SULTAN_HAGRY\backups\database\monthly
mkdir D:\SULTAN_HAGRY\backups\evidence\daily

# Linux
mkdir -p /var/backups/shaniya/database/{daily,weekly,monthly}
mkdir -p /var/backups/shaniya/evidence/daily
```

### 2. ضبط الصلاحيات (Linux فقط)

```bash
chmod +x scripts/backup_database.sh
chmod +x scripts/backup_evidence.sh
```

---

## الجدولة

### Windows - Task Scheduler

#### نسخ قاعدة البيانات (يومياً 2:00 ص)

```powershell
schtasks /create /tn "Shaniya Backup Database" /tr "D:\SULTAN_HAGRY\scripts\backup_database.bat" /sc daily /st 02:00 /ru SYSTEM
```

#### نسخ الأدلة (يومياً 3:00 ص)

```powershell
schtasks /create /tn "Shaniya Backup Evidence" /tr "D:\SULTAN_HAGRY\scripts\backup_evidence.bat" /sc daily /st 03:00 /ru SYSTEM
```

#### عرض المهام المجدولة

```powershell
schtasks /query /tn "Shaniya*"
```

#### حذف مهمة

```powershell
schtasks /delete /tn "Shaniya Backup Database" /f
```

---

### Linux - Cron

#### تحرير جدول Cron

```bash
crontab -e
```

#### إضافة المهام

```cron
# نسخ قاعدة البيانات يومياً 2:00 ص
0 2 * * * /path/to/scripts/backup_database.sh >> /var/log/shaniya_backup.log 2>&1

# نسخ الأدلة يومياً 3:00 ص
0 3 * * * /path/to/scripts/backup_evidence.sh >> /var/log/shaniya_backup.log 2>&1
```

#### عرض المهام المجدولة

```bash
crontab -l
```

---

## الاختبار اليدوي

### Windows

```powershell
# اختبار نسخ قاعدة البيانات
D:\SULTAN_HAGRY\scripts\backup_database.bat

# اختبار نسخ الأدلة
D:\SULTAN_HAGRY\scripts\backup_evidence.bat
```

### Linux

```bash
# اختبار نسخ قاعدة البيانات
./scripts/backup_database.sh

# اختبار نسخ الأدلة
./scripts/backup_evidence.sh
```

---

## استعادة النسخة الاحتياطية

### قاعدة البيانات

#### Windows

```powershell
# فك الضغط
Expand-Archive -Path "backups\database\daily\shaniya_2026-02-10.sql.zip" -DestinationPath "temp\"

# استعادة
docker exec -i postgres psql -U app_admin -d shaniya < temp\shaniya_2026-02-10.sql
```

#### Linux

```bash
# فك الضغط
gunzip -c backups/database/daily/shaniya_2026-02-10.sql.gz > temp.sql

# استعادة
psql -U app_admin -h localhost -p 5434 shaniya < temp.sql
```

### مستودع الأدلة

#### Windows

```powershell
# فك الضغط
Expand-Archive -Path "backups\evidence\daily\evidence_vault_2026-02-10.zip" -DestinationPath "media\"
```

#### Linux

```bash
# فك الضغط
tar -xzf backups/evidence/daily/evidence_vault_2026-02-10.tar.gz -C media/
```

---

## المراقبة

### فحص السجلات

#### Windows

```powershell
# سجلات قاعدة البيانات
type D:\SULTAN_HAGRY\backups\database\logs\backup_2026-02-10.log

# سجلات الأدلة
type D:\SULTAN_HAGRY\backups\evidence\logs\backup_2026-02-10.log
```

#### Linux

```bash
# سجلات قاعدة البيانات
cat /var/backups/shaniya/database/logs/backup_2026-02-10.log

# سجلات الأدلة
cat /var/backups/shaniya/evidence/logs/backup_2026-02-10.log
```

### فحص حجم النسخ الاحتياطية

```powershell
# Windows
Get-ChildItem -Path "D:\SULTAN_HAGRY\backups" -Recurse | Measure-Object -Property Length -Sum

# Linux
du -sh /var/backups/shaniya/*
```

---

## استراتيجية الاحتفاظ

| النوع | المدة | الموقع |
|-------|-------|---------|
| يومي | 7 أيام | `daily/` |
| أسبوعي | 4 أسابيع | `weekly/` |
| شهري | 12 شهر | `monthly/` |

**ملاحظة**: النسخ الأسبوعية والشهرية يتم إنشاؤها تلقائياً في سكريبتات Linux.

---

## استكشاف الأخطاء

### خطأ: "Access Denied"

**الحل**: تشغيل السكريبت بصلاحيات المسؤول

### خطأ: "Database connection failed"

**الحل**: التحقق من تشغيل PostgreSQL

```bash
docker ps | grep postgres
```

### خطأ: "Disk space full"

**الحل**: حذف النسخ القديمة يدوياً أو زيادة مساحة التخزين

---

## الأمان

✅ **التوصيات**:

- تخزين النسخ الاحتياطية في موقع منفصل (خادم آخر أو سحابة)
- تشفير النسخ الاحتياطية قبل النقل
- تقييد الصلاحيات على مجلدات النسخ الاحتياطي
- اختبار الاستعادة شهرياً

---

## الدعم

للمساعدة أو الإبلاغ عن مشاكل، راجع سجلات النسخ الاحتياطي في:

- Windows: `D:\SULTAN_HAGRY\backups\{database|evidence}\logs\`
- Linux: `/var/backups/shaniya/{database|evidence}/logs/`
