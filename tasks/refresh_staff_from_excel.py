
import os
import django
import sys
import pandas as pd
import numpy as np

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from coredata.models import Staff, JobTitle, AcademicYear
from django.contrib.auth.models import User, Group
from django.db import transaction

def normalize_name(name):
    if not name or pd.isna(name): return ""
    res = str(name).replace('أ', 'ا').replace('إ', 'ا').replace('آ', 'ا').replace('ة', 'ه').replace('ى', 'ي')
    res = res.replace('.', '').replace(',', '').replace('  ', ' ')
    res = "".join(res.split())
    return res

def refresh_staff():
    print("--- البدء في التطهير الكامل والمزامنة الصارمة (124 موظف + أدمن) ---")
    
    file_master = 'الارشيف/Doc_School/school_DATA/موظفي لمدرسة.xlsx'
    file_details = 'الارشيف/Doc_School/school_DATA/stuff_03.xlsx'
    
    if not os.path.exists(file_master) or not os.path.exists(file_details):
        print(f"خطأ: أحد الملفات غير موجود!")
        return

    df_master = pd.read_excel(file_master)
    df_details = pd.read_excel(file_details)
    
    print(f"قائمة الماستر تحتوي على {len(df_master)} اسم.")

    with transaction.atomic():
        # 1. Collect authorized usernames/names
        authorized_usernames = set()
        for _, row in df_master.iterrows():
            if not pd.isna(row['User_Name']):
                authorized_usernames.add(str(row['User_Name']).strip())

        # 2. Delete ALL staff and job titles (Reset)
        Staff.objects.all().delete()
        JobTitle.objects.all().delete()
        
        # 3. Purge unauthorized users
        # Save admin first
        admins = User.objects.filter(is_superuser=True)
        admin_usernames = {u.username for u in admins}
        print(f"الحسابات الإدارية المحمية: {', '.join(admin_usernames)}")
        
        # Deletion
        deleted_count = 0
        all_users = list(User.objects.all())
        for u in all_users:
            if u.username not in authorized_usernames and u.username not in admin_usernames:
                u.delete()
                deleted_count += 1
        print(f"تم حذف {deleted_count} مستخدم غير مصرح لهم.")

        # 4. Re-import from Master
        details_map = {normalize_name(row['stuff _name']): row for _, row in df_details.iterrows()}
        
        created_count = 0
        for _, row in df_master.iterrows():
            full_name = str(row['Full_Name']).strip()
            norm_name = normalize_name(full_name)
            job_name = str(row['Job']).strip()
            username = str(row['User_Name']).strip()
            
            details = details_map.get(norm_name)
            email = None
            job_number = None
            national_no = None
            phone_no = str(row.get('Phone_No', '')) if not pd.isna(row.get('Phone_No')) and str(row.get('Phone_No')) != "1" else ""
            
            if details is not None:
                email_val = str(details.get('email', '')).strip() if not pd.isna(details.get('email')) else ""
                if email_val and "@" in email_val: email = email_val
                
                job_num_val = str(details.get('job_no', '')).strip() if not pd.isna(details.get('job_no')) else ""
                if job_num_val: job_number = job_num_val
                
                nat_no_val = str(details.get('national_no', '')).strip() if not pd.isna(details.get('national_no')) else ""
                if nat_no_val: national_no = nat_no_val

            jt, _ = JobTitle.objects.get_or_create(title=job_name, is_canonical=True)
            
            # Create Staff and User if missing
            staff_user = User.objects.filter(username=username).first()
            if not staff_user:
                # Create user with password from excel if it doesn't exist
                password = str(row['User_Password']) if not pd.isna(row['User_Password']) else "123"
                staff_user = User.objects.create_user(username=username, password=password)
                staff_user.first_name = full_name.split()[0]
                staff_user.last_name = full_name.split()[-1] if len(full_name.split()) > 1 else ""
                staff_user.save()

            staff = Staff.objects.create(
                user=staff_user,
                name=full_name,
                job_title=jt,
                job_number=job_number,
                national_no=national_no,
                email=email,
                phone_no=phone_no if phone_no else None
            )
            
            # Assign Groups
            if "مدير" in job_name or "نائب" in job_name:
                grp, _ = Group.objects.get_or_create(name='الإدارة العليا')
            elif "منسق" in job_name:
                grp, _ = Group.objects.get_or_create(name='الإدارة الوسطى')
            elif "معلم" in job_name:
                grp, _ = Group.objects.get_or_create(name='المعلمون')
            else:
                grp, _ = Group.objects.get_or_create(name='الموارد البشرية')
            staff_user.groups.add(grp)
            
            created_count += 1

    print(f"\n--- ملخص العملية النهائي ---")
    print(f"إجمالي الموظفين (Staff): {Staff.objects.count()}")
    print(f"إجمالي المستخدمين (User): {User.objects.count()}")
    print(f"تطابق الموظفين مع القائمة المعتمدة: {'نعم' if Staff.objects.count() == 124 else 'لا'}")

if __name__ == "__main__":
    refresh_staff()
