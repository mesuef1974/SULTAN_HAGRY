# اختبارات التحمل - دليل الاستخدام

## المتطلبات

```bash
pip install locust
```

## تشغيل الاختبارات

### 1. تشغيل الخادم المحلي

في نافذة طرفية منفصلة:

```bash
python manage.py runserver
```

### 2. تشغيل Locust

```bash
cd tests/stress
locust -f locustfile.py --host=http://127.0.0.1:8000
```

### 3. فتح واجهة Locust

افتح المتصفح على: `http://localhost:8089`

## إعدادات الاختبار المقترحة

### اختبار خفيف (Warm-up)

- **Number of users**: 10
- **Spawn rate**: 2 users/second
- **Duration**: 2 minutes

### اختبار متوسط

- **Number of users**: 30
- **Spawn rate**: 5 users/second
- **Duration**: 5 minutes

### اختبار التحمل الكامل

- **Number of users**: 50
- **Spawn rate**: 10 users/second
- **Duration**: 10 minutes

## المقاييس المهمة

راقب هذه المؤشرات في واجهة Locust:

1. **Response Time (ms)**
   - المتوسط: يجب أن يكون < 2000ms
   - الحد الأقصى: يجب أن يكون < 5000ms

2. **Requests per Second (RPS)**
   - يجب أن يكون مستقراً

3. **Failure Rate**
   - يجب أن يكون < 1%

## أنواع المستخدمين

الملف يحتوي على 3 أنواع من المستخدمين:

1. **PlatformUser**: مستخدم عادي (معلم/مشرف)
2. **HeavyUser**: مستخدم يقوم بعمليات ثقيلة
3. **ReadOnlyUser**: مستخدم للقراءة فقط

## ملاحظات مهمة

⚠️ **قبل الاختبار**:

1. تأكد من وجود بيانات تجريبية في قاعدة البيانات
2. أنشئ مستخدمين للاختبار:
   - `test_user` / `test_password`
   - `test_admin` / `test_password`
   - `test_viewer` / `test_password`

⚠️ **أثناء الاختبار**:

- راقب استهلاك الذاكرة والمعالج
- تحقق من سجلات Django للأخطاء
- راقب استعلامات قاعدة البيانات

## تصدير النتائج

يمكنك تصدير النتائج من واجهة Locust:

- **Download Data** → CSV
- **Charts** → Screenshots

## استكشاف الأخطاء

### خطأ في الاتصال

```bash
# تأكد من أن الخادم يعمل
python manage.py runserver
```

### بطء شديد

- قلل عدد المستخدمين
- تحقق من استعلامات قاعدة البيانات (Django Debug Toolbar)
- راجع إعدادات Gunicorn Workers
