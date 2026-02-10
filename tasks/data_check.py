import os
import django
import sys

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from coredata.models import Staff, Committee, JobTitle
from django.db.models import Count

def check_duplicates():
    print(f"Total Staff Records: {Staff.objects.count()}")
    # Check by job_number
    staff_by_job_no = Staff.objects.values('job_number').annotate(count=Count('id')).filter(count__gt=1)
    for entry in staff_by_job_no:
        if entry['job_number']:
            print(f"Duplicate Job Number: {entry['job_number']} (Count: {entry['count']})")
    
    # Check by email
    staff_by_email = Staff.objects.values('email').annotate(count=Count('id')).filter(count__gt=1)
    for entry in staff_by_email:
        if entry['email']:
            print(f"Duplicate Email: {entry['email']} (Count: {entry['count']})")
            
    # Check by name
    staff_by_name = Staff.objects.values('name').annotate(count=Count('id')).filter(count__gt=1)
    for entry in staff_by_name:
        print(f"Duplicate Name: {entry['name']} (Count: {entry['count']})")

    print(f"Total Committee Records: {Committee.objects.count()}")
    comm_by_name = Committee.objects.values('name').annotate(count=Count('id')).filter(count__gt=1)
    for entry in comm_by_name:
        print(f"Duplicate Committee Name: {entry['name']} (Count: {entry['count']})")

def verify_rbac():
    print("\n--- Verifying RBAC Mapping ---")
    staff_list = Staff.objects.all()
    for person in staff_list:
        if person.user and person.job_title:
            required_groups = person.job_title.groups.all()
            user_groups = person.user.groups.all()
            missing = [g.name for g in required_groups if g not in user_groups]
            if missing:
                print(f"Staff {person.name} is missing groups: {missing}")

if __name__ == "__main__":
    check_duplicates()
    verify_rbac()
