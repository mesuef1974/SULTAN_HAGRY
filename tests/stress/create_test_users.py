"""
سكريبت لإنشاء مستخدمين تجريبيين لاختبارات التحمل
Script to create test users for stress testing
"""

import os
import django
import sys

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from django.contrib.auth.models import User, Group

def create_test_users():
    """إنشاء مستخدمين تجريبيين للاختبار"""
    
    test_users = [
        {
            "username": "test_user",
            "password": "test_password",
            "email": "test_user@test.com",
            "is_staff": True,
            "is_superuser": False
        },
        {
            "username": "test_admin",
            "password": "test_password",
            "email": "test_admin@test.com",
            "is_staff": True,
            "is_superuser": True
        },
        {
            "username": "test_viewer",
            "password": "test_password",
            "email": "test_viewer@test.com",
            "is_staff": True,
            "is_superuser": False
        }
    ]
    
    print("إنشاء المستخدمين التجريبيين...")
    
    for user_data in test_users:
        username = user_data["username"]
        
        # حذف المستخدم إذا كان موجوداً
        if User.objects.filter(username=username).exists():
            User.objects.filter(username=username).delete()
            print(f"  ✓ تم حذف المستخدم القديم: {username}")
        
        # إنشاء المستخدم الجديد
        user = User.objects.create_user(
            username=user_data["username"],
            email=user_data["email"],
            password=user_data["password"],
            is_staff=user_data["is_staff"],
            is_superuser=user_data["is_superuser"]
        )
        
        print(f"  ✓ تم إنشاء المستخدم: {username}")
    
    print("\n✅ تم إنشاء جميع المستخدمين التجريبيين بنجاح!")
    print("\nبيانات الدخول:")
    print("-" * 50)
    for user_data in test_users:
        print(f"  Username: {user_data['username']}")
        print(f"  Password: {user_data['password']}")
        print(f"  Role: {'Admin' if user_data['is_superuser'] else 'Staff'}")
        print("-" * 50)

if __name__ == "__main__":
    create_test_users()
