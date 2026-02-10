import csv
import os
from django.core.management.base import BaseCommand
from coredata.models import JobTitle, EvidenceFile

class Command(BaseCommand):
    help = 'Creates JobTitles and EvidenceFiles from CSV.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("\n--- Step 1: Populating Files from CSV ---"))
        self.populate_from_csv()
        self.stdout.write(self.style.SUCCESS("\n--- Data Population Complete! ---"))

    def populate_from_csv(self):
        """
        Reads the CSV to create EvidenceFiles and JobTitles.
        """
        csv_path = r'الارشيف/Doc_School/ملفات المدرسة.csv'
        if not os.path.exists(csv_path):
            self.stdout.write(self.style.ERROR(f"CSV file not found at {csv_path}"))
            return

        JOB_NORMALIZATION = {
            "الاخصائي الاجتماعي": "أخصائي اجتماعي",
            "اخصائي اجتماعي": "أخصائي اجتماعي",
            "الاخصائي النفسي": "اخصائي نفسي",
            "أمين المخزن": "امين مخزن",
            # ... other mappings if needed ...
        }

        with open(csv_path, 'r', encoding='utf-8-sig') as f:
            content = f.read(1024)
            f.seek(0)
            dialect = ';' if ';' in content else ','
            reader = csv.DictReader(f, delimiter=dialect)
            
            for row in reader:
                raw_job = row.get('Pos')
                raw_file = row.get('Files')
                if not raw_job or not raw_file: continue

                job_title_text = raw_job.strip()
                file_name_text = raw_file.strip()

                normalized_job = JOB_NORMALIZATION.get(job_title_text, job_title_text).strip()
                JobTitle.objects.get_or_create(title=normalized_job)
                EvidenceFile.objects.get_or_create(name=file_name_text)
                
        self.stdout.write(self.style.SUCCESS("CSV Population Completed."))