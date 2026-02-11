
from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import User, Group
from .models import (
    Staff, OperationalPlanItems, Committee,
    JobTitle, EvidenceFile,
    AcademicYear, StrategicGoal, OperationalGoal,
    Student, EvidenceDocument, GroupExtension
)
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin

# --- Admin Models ---

@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_active', 'start_date', 'end_date')
    list_editable = ('is_active',)

@admin.register(StrategicGoal)
class StrategicGoalAdmin(admin.ModelAdmin):
    list_display = ('code', 'academic_year', 'title')
    list_filter = ('academic_year',)
    search_fields = ('title', 'code')

@admin.register(OperationalGoal)
class OperationalGoalAdmin(admin.ModelAdmin):
    list_display = ('code', 'strategic_goal', 'title')
    list_filter = ('strategic_goal__academic_year',)
    search_fields = ('title', 'code')

# NOTE: The custom admin site is disabled because it runs DB queries on startup.
# This is a common cause of crashes in serverless environments.
# We will re-enable this later in a safe way.
#
# class CoreDataAdminSite(admin.AdminSite):
#     ...
# admin.site = CoreDataAdminSite()


@admin.register(Staff)
class StaffAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    list_display = ('name', 'job_title', 'job_number', 'email')
    search_fields = ('name', 'job_number', 'email')
    list_filter = ('job_title',)
    raw_id_fields = ('user', 'job_title')

@admin.register(OperationalPlanItems)
class OperationalPlanItemsAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    list_display = ('code', 'academic_year', 'rank_name', 'status', 'executor_committee')
    list_filter = ('academic_year', 'status', 'rank_name', 'executor_committee')
    search_fields = ('code', 'procedure')
    autocomplete_fields = ['executor_committee', 'evaluator_committee']

@admin.register(JobTitle)
class JobTitleAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    list_display = ('code', 'title')
    search_fields = ('title', 'code')

@admin.register(EvidenceFile)
class EvidenceFileAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    list_display = ('code', 'name')
    search_fields = ('name', 'code')

@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    list_display = ('name_ar', 'grade', 'section', 'national_no')
    list_filter = ('grade', 'section')
    search_fields = ('name_ar', 'national_no')

@admin.register(EvidenceDocument)
class EvidenceDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'evidence_type', 'user', 'academic_year')
    list_filter = ('academic_year', 'evidence_type', 'user')
    search_fields = ('title', 'description', 'tags')
    autocomplete_fields = ['user', 'evidence_type']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.user = request.user
        super().save_model(request, obj, form, change)

@admin.register(Committee)
class CommitteeAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    list_display = ('code', 'name', 'academic_year')
    search_fields = ('name', 'code')
    filter_horizontal = ('members',)
    list_filter = ('academic_year',)
    autocomplete_fields = ['members']