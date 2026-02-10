from django.core.management.base import BaseCommand
from coredata.models import EvidenceFile

class Command(BaseCommand):
    help = 'Adds "Question Bank" file category'

    def handle(self, *args, **options):
        file_name = "بنك الأسئلة"
        evidence_file, created = EvidenceFile.objects.get_or_create(name=file_name)
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created new file category: '{file_name}'"))
        else:
            self.stdout.write(f"File category '{file_name}' already exists.")