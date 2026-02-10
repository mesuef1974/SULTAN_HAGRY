# دليل ربط GitHub بـ Docker

## نظرة عامة

هذا الدليل يشرح كيفية ربط GitHub بـ Docker لإنشاء CI/CD pipeline آلي.

---

## الإعداد الأولي

### 1. إنشاء Personal Access Token (PAT)

1. اذهب إلى GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. انقر على "Generate new token (classic)"
3. أعط التوكن اسماً: `Docker GHCR Token`
4. اختر الصلاحيات:
   - ✅ `write:packages` - لنشر الصور
   - ✅ `read:packages` - لقراءة الصور
   - ✅ `delete:packages` - لحذف الصور (اختياري)
5. انقر "Generate token"
6. **احفظ التوكن** - لن تراه مرة أخرى!

### 2. إضافة Secret إلى المستودع (اختياري)

> **ملاحظة**: GitHub Actions يوفر `GITHUB_TOKEN` تلقائياً، لكن يمكنك إضافة توكن مخصص إذا أردت.

1. اذهب إلى المستودع → Settings → Secrets and variables → Actions
2. انقر "New repository secret"
3. الاسم: `GHCR_TOKEN`
4. القيمة: الصق التوكن
5. انقر "Add secret"

---

## استخدام GitHub Actions

### الملف الموجود

تم إنشاء ملف workflow في:

```
.github/workflows/docker-build.yml
```

### كيف يعمل

عند كل `push` إلى `main` أو `dev`:

1. ✅ يتم checkout الكود
2. ✅ تسجيل الدخول إلى ghcr.io
3. ✅ بناء صورة Docker
4. ✅ نشر الصورة إلى GitHub Container Registry

### Tags التلقائية

| الحدث | Tag المُنشأ |
|-------|-------------|
| Push to main | `latest`, `main` |
| Push to dev | `dev` |
| Tag v1.0.0 | `v1.0.0`, `1.0`, `latest` |
| Commit SHA | `main-abc1234` |

---

## استخدام الصورة المنشورة

### 1. تسجيل الدخول إلى ghcr.io

```bash
# استخدام PAT
echo YOUR_PAT_TOKEN | docker login ghcr.io -u YOUR_USERNAME --password-stdin

# أو استخدام GitHub CLI
gh auth token | docker login ghcr.io -u YOUR_USERNAME --password-stdin
```

### 2. Pull الصورة

```bash
# استبدل USERNAME و REPO_NAME
docker pull ghcr.io/USERNAME/REPO_NAME:latest
```

### 3. تحديث docker-compose.yml

```yaml
services:
  django:
    # بدلاً من build:
    image: ghcr.io/mesuef1974/sultan_hagry:latest
    # باقي الإعدادات...
```

---

## الأوامر المفيدة

### عرض الصور المتاحة

```bash
# عبر GitHub CLI
gh api /user/packages/container/REPO_NAME/versions

# أو زيارة
https://github.com/USERNAME?tab=packages
```

### حذف صورة قديمة

```bash
# عبر GitHub CLI
gh api -X DELETE /user/packages/container/REPO_NAME/versions/VERSION_ID
```

### Pull صورة محددة

```bash
# آخر إصدار
docker pull ghcr.io/USERNAME/REPO_NAME:latest

# إصدار محدد
docker pull ghcr.io/USERNAME/REPO_NAME:v1.0.0

# من branch dev
docker pull ghcr.io/USERNAME/REPO_NAME:dev
```

---

## التشغيل المحلي

### باستخدام الصورة من ghcr.io

```bash
# 1. تسجيل الدخول
echo YOUR_PAT | docker login ghcr.io -u USERNAME --password-stdin

# 2. Pull الصورة
docker pull ghcr.io/USERNAME/REPO_NAME:latest

# 3. تشغيل docker-compose
docker-compose up -d
```

---

## استكشاف الأخطاء

### خطأ: "authentication required"

**الحل**:

```bash
docker logout ghcr.io
echo YOUR_PAT | docker login ghcr.io -u USERNAME --password-stdin
```

### خطأ: "denied: permission_denied"

**الحل**: تأكد من صلاحيات التوكن (`write:packages`)

### خطأ: "workflow failed"

**الحل**:

1. افتح GitHub → Actions
2. انقر على الـ workflow الفاشل
3. راجع السجلات للتفاصيل

---

## الفوائد

✅ **بناء تلقائي**: لا حاجة لبناء الصور محلياً
✅ **إصدارات منظمة**: كل commit له صورة خاصة
✅ **سهولة النشر**: pull الصورة مباشرة على الخادم
✅ **CI/CD**: اختبارات آلية قبل النشر
✅ **مجاني**: للمستودعات العامة

---

## الخطوات التالية

1. ✅ Push الكود إلى GitHub
2. ✅ راقب GitHub Actions (تبويب Actions)
3. ✅ تحقق من الصورة في Packages
4. ✅ استخدم الصورة في الإنتاج

---

## مثال كامل

```bash
# 1. Push الكود
git add .
git commit -m "Add GitHub Actions workflow"
git push origin main

# 2. انتظر اكتمال البناء (GitHub Actions)

# 3. على الخادم
echo YOUR_PAT | docker login ghcr.io -u USERNAME --password-stdin
docker pull ghcr.io/USERNAME/REPO_NAME:latest
docker-compose up -d
```

---

## الدعم

للمزيد من المعلومات:

- [GitHub Container Registry Docs](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
- [GitHub Actions Docs](https://docs.github.com/en/actions)
