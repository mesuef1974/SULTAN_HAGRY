# دليل نشر منصة الشحانية الذكية (Production Deployment Guide)

## البيئة التقنية

- **Python**: 3.12+
- **Django**: 6.0.2
- **خادم التطبيق**: Gunicorn 23.0.0 + Uvicorn Workers
- **قاعدة البيانات**: PostgreSQL 15+
- **المهام الخلفية**: Celery + Redis

## خطوات النشر باستخدام Docker

### 1. بناء الحاويات

```bash
cd docker
docker-compose build
```

### 2. تشغيل المنصة

```bash
docker-compose up -d
```

### 3. التحقق من الحالة

```bash
docker-compose ps
docker-compose logs django
```

## إعدادات الإنتاج

### متغيرات البيئة المطلوبة

في ملف `.env`:

```
DJANGO_SECRET_KEY=<your-secret-key>
DJANGO_DEBUG=0
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
POSTGRES_DB=shaniya
POSTGRES_USER=app_admin
POSTGRES_PASSWORD=<strong-password>
CELERY_BROKER_URL=redis://redis:6379/0
```

### إعدادات Gunicorn

- **Workers**: 3 (يمكن تعديلها بناءً على عدد المعالجات)
- **Worker Class**: uvicorn.workers.UvicornWorker (لدعم ASGI)
- **Bind**: 0.0.0.0:8000
- **Access Log**: تفعيل السجلات للمراقبة

## الأمان

✅ تم تفعيل:

- تشفير الحقول الحساسة (AES-256)
- بصمة النزاهة الرقمية
- HTTPS (يجب ضبطه على مستوى Nginx/Load Balancer)
- CSRF Protection
- Session Security

## المراقبة

- **صحة المنصة**: `/health/`
- **لوحة Celery (Flower)**: `http://localhost:5555`
- **إدارة قاعدة البيانات (Adminer)**: `http://localhost:8080`

## النسخ الاحتياطي

يُنصح بجدولة نسخ احتياطي يومي لـ:

1. قاعدة البيانات PostgreSQL
2. مجلد الأدلة (`media/evidence_vault/`)

```bash
# مثال: نسخ احتياطي لقاعدة البيانات
docker-compose exec postgres pg_dump -U app_admin shaniya > backup_$(date +%Y%m%d).sql
```

## الترقية

```bash
# سحب آخر التحديثات
git pull origin main

# إعادة بناء الحاويات
docker-compose build

# إعادة التشغيل
docker-compose down
docker-compose up -d

# تطبيق الترحيلات
docker-compose exec django python manage.py migrate
```

---
**ملاحظة**: هذا الدليل يفترض استخدام Docker. للنشر المباشر على الخادم، يُنصح باستخدام Nginx كـ Reverse Proxy أمام Gunicorn.
