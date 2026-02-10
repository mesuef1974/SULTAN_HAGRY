"""
اختبارات التحمل لمنصة الشحانية الذكية
Stress Testing for Al-Shahaniya Smart Platform

هذا الملف يحتوي على سيناريوهات اختبار التحمل باستخدام Locust.
"""

from locust import HttpUser, task, between
import random


class PlatformUser(HttpUser):
    """
    محاكاة مستخدم عادي للمنصة (معلم أو مشرف)
    """
    wait_time = between(1, 3)  # انتظار من 1 إلى 3 ثوانٍ بين المهام
    
    def on_start(self):
        """يتم تنفيذها عند بدء كل مستخدم افتراضي"""
        # محاكاة تسجيل الدخول
        self.login()
    
    def login(self):
        """تسجيل الدخول"""
        # ملاحظة: استخدم بيانات تجريبية حقيقية من قاعدة البيانات
        response = self.client.get("/admin/login/")
        
        # في حالة وجود CSRF token
        if response.status_code == 200:
            self.client.post("/admin/login/", {
                "username": "test_user",
                "password": "test_password",
            })
    
    @task(3)
    def view_dashboard(self):
        """عرض لوحة التحكم - المهمة الأكثر شيوعاً"""
        self.client.get("/admin/")
    
    @task(2)
    def view_operational_plan(self):
        """عرض الخطة التشغيلية"""
        self.client.get("/admin/coredata/operationalplanitems/")
    
    @task(2)
    def view_committees(self):
        """عرض اللجان"""
        self.client.get("/admin/coredata/committee/")
    
    @task(1)
    def view_staff(self):
        """عرض الموظفين"""
        self.client.get("/admin/coredata/staff/")
    
    @task(1)
    def view_evidence_documents(self):
        """عرض مستودع الأدلة"""
        self.client.get("/admin/coredata/evidencedocument/")


class HeavyUser(HttpUser):
    """
    محاكاة مستخدم يقوم بعمليات ثقيلة (رفع ملفات، تحديثات)
    """
    wait_time = between(2, 5)
    
    def on_start(self):
        self.login()
    
    def login(self):
        response = self.client.get("/admin/login/")
        if response.status_code == 200:
            self.client.post("/admin/login/", {
                "username": "test_admin",
                "password": "test_password",
            })
    
    @task(2)
    def view_plan_item_detail(self):
        """عرض تفاصيل بند من الخطة"""
        # استخدام ID عشوائي (يجب تعديله بناءً على البيانات الفعلية)
        item_id = random.randint(1, 100)
        self.client.get(f"/admin/coredata/operationalplanitems/{item_id}/change/")
    
    @task(1)
    def search_plan_items(self):
        """البحث في بنود الخطة"""
        self.client.get("/admin/coredata/operationalplanitems/?q=test")
    
    @task(1)
    def view_health_check(self):
        """فحص صحة المنصة"""
        self.client.get("/health/")


class ReadOnlyUser(HttpUser):
    """
    محاكاة مستخدم للقراءة فقط (مقيّم أو مراقب)
    """
    wait_time = between(1, 2)
    
    def on_start(self):
        self.login()
    
    def login(self):
        response = self.client.get("/admin/login/")
        if response.status_code == 200:
            self.client.post("/admin/login/", {
                "username": "test_viewer",
                "password": "test_password",
            })
    
    @task(4)
    def browse_plan_items(self):
        """تصفح بنود الخطة"""
        self.client.get("/admin/coredata/operationalplanitems/")
    
    @task(2)
    def view_reports(self):
        """عرض التقارير"""
        self.client.get("/admin/")
    
    @task(1)
    def view_committees_list(self):
        """عرض قائمة اللجان"""
        self.client.get("/admin/coredata/committee/")
