
import os
import django
from django.db import connection

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from diagnostics.models import (
    JobTitle, Staff, AcademicYear, StrategicGoal, OperationalGoal, 
    Committee, Student, OperationalPlanItems, EvidenceFile, EvidenceDocument
)
from django.contrib.auth.models import User

def migrate_data():
    with connection.cursor() as cursor:
        # 1. Job Titles
        print("Migrating Job Titles...")
        cursor.execute("SELECT id, title, code, description, is_canonical FROM job_titles")
        for row in cursor.fetchall():
            jt, created = JobTitle.objects.get_or_create(
                id=row[0],
                defaults={
                    'title': row[1],
                    'code': row[2],
                    'description': row[3],
                    'is_canonical': row[4]
                }
            )

        # 2. Staff
        print("Migrating Staff...")
        cursor.execute("SELECT id, name, code, nationality, job_number, email, national_no, phone_no, account_no, job_title_id, user_id FROM staff")
        for row in cursor.fetchall():
            # Encrypted fields will be handled by the model's to_prep_value/from_db_value if we use ORM
            # Since we are reading from DB, if they were already encrypted we might have an issue, 
            # but usually backups are plain text or we handle it. 
            # In the old system they were plain text likely.
            
            s, created = Staff.objects.get_or_create(
                id=row[0],
                defaults={
                    'name': row[1],
                    'code': row[2],
                    'nationality': row[3],
                    'job_number': row[4],
                    'email': row[5],
                    'national_no': row[6],
                    'phone_no': row[7],
                    'account_no': row[8],
                    'job_title_id': row[9],
                    'user_id': row[10]
                }
            )

        # 3. Academic Year
        print("Migrating Academic Years...")
        cursor.execute("SELECT id, name, start_date, end_date, is_active, code FROM coredata_academicyear")
        for row in cursor.fetchall():
            ay, created = AcademicYear.objects.get_or_create(
                id=row[0],
                defaults={
                    'name': row[1],
                    'start_date': row[2],
                    'end_date': row[3],
                    'is_active': row[4],
                    'code': row[5]
                }
            )

        # 4. Strategic Goals
        print("Migrating Strategic Goals...")
        cursor.execute("SELECT id, title, goal_no, code, academic_year_id FROM coredata_strategicgoal")
        for row in cursor.fetchall():
            sg, created = StrategicGoal.objects.get_or_create(
                id=row[0],
                defaults={
                    'title': row[1],
                    'goal_no': row[2],
                    'code': row[3],
                    'academic_year_id': row[4]
                }
            )

        # 5. Operational Goals
        print("Migrating Operational Goals...")
        cursor.execute("SELECT id, title, indicator_no, code, strategic_goal_id FROM coredata_operationalgoal")
        for row in cursor.fetchall():
            og, created = OperationalGoal.objects.get_or_create(
                id=row[0],
                defaults={
                    'title': row[1],
                    'indicator_no': row[2],
                    'code': row[3],
                    'strategic_goal_id': row[4]
                }
            )

        # 6. Committees
        print("Migrating Committees...")
        cursor.execute("SELECT id, name, code, description, academic_year_id FROM committees")
        for row in cursor.fetchall():
            c, created = Committee.objects.get_or_create(
                id=row[0],
                defaults={
                    'name': row[1],
                    'code': row[2],
                    'description': row[3],
                    'academic_year_id': row[4]
                }
            )
            
        # 7. Students
        print("Migrating Students...")
        cursor.execute("SELECT id, national_no, name_ar, name_en, date_of_birth, grade, section, needs, parent_national_no, parent_name, parent_relation, parent_phone, parent_email FROM students")
        for row in cursor.fetchall():
            st, created = Student.objects.get_or_create(
                id=row[0],
                defaults={
                    'national_no': row[1],
                    'name_ar': row[2],
                    'name_en': row[3],
                    'date_of_birth': row[4],
                    'grade': row[5],
                    'section': row[6],
                    'needs': row[7],
                    'parent_national_no': row[8],
                    'parent_name': row[9],
                    'parent_relation': row[10],
                    'parent_phone': row[11],
                    'parent_email': row[12]
                }
            )

        # 8. Evidence File (Categories)
        print("Migrating Evidence Categories...")
        cursor.execute("SELECT id, name, code, description FROM evidence_files")
        for row in cursor.fetchall():
            ef, created = EvidenceFile.objects.get_or_create(
                id=row[0],
                defaults={
                    'name': row[1],
                    'code': row[2],
                    'description': row[3]
                }
            )

        # 9. Evidence Documents
        print("Migrating Evidence Documents...")
        cursor.execute("SELECT id, title, file, original_filename, file_size, file_hash, tags, description, created_at, academic_year_id, evidence_type_id, user_id FROM evidence_documents")
        for row in cursor.fetchall():
            ed, created = EvidenceDocument.objects.get_or_create(
                id=row[0],
                defaults={
                    'title': row[1],
                    'file': row[2],
                    'original_filename': row[3],
                    'file_size': row[4],
                    'file_hash': row[5],
                    'tags': row[6],
                    'description': row[7],
                    'created_at': row[8],
                    'academic_year_id': row[9],
                    'evidence_type_id': row[10],
                    'user_id': row[11]
                }
            )

        # 10. Operational Plan Items
        print("Migrating Operational Plan Items...")
        cursor.execute("""
            SELECT id, rank_name, procedure, code, executor, date_range, follow_up, comments, 
            evidence_type, evidence_source_employee, evidence_source_file, evaluation, 
            evaluation_notes, evidence_requested, evidence_requested_at, evidence_request_note, 
            last_review_date, digital_seal, status, academic_year_id, evaluator_committee_id, 
            evidence_document_id, executor_committee_id, operational_goal_link_id, strategic_goal_link_id 
            FROM operational_plan_items
        """)
        for row in cursor.fetchall():
            opi, created = OperationalPlanItems.objects.get_or_create(
                id=row[0],
                defaults={
                    'rank_name': row[1],
                    'procedure': row[2],
                    'code': row[3],
                    'executor': row[4],
                    'date_range': row[5],
                    'follow_up': row[6],
                    'comments': row[7],
                    'evidence_type': row[8],
                    'evidence_source_employee': row[9],
                    'evidence_source_file': row[10],
                    'evaluation': row[11],
                    'evaluation_notes': row[12],
                    'evidence_requested': row[13],
                    'evidence_requested_at': row[14],
                    'evidence_request_note': row[15],
                    'last_review_date': row[16],
                    'digital_seal': row[17],
                    'status': row[18],
                    'academic_year_id': row[19],
                    'evaluator_committee_id': row[20],
                    'evidence_document_id': row[21],
                    'executor_committee_id': row[22],
                    'operational_goal_link_id': row[23],
                    'strategic_goal_link_id': row[24]
                }
            )

    print("Migration completed successfully!")

if __name__ == "__main__":
    migrate_data()