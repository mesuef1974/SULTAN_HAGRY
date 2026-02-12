from django.contrib import admin
from .models import (
    JobTitle, EvidenceFile, Staff, AcademicYear, 
    StrategicGoal, OperationalGoal, Committee, 
    EvidenceDocument, OperationalPlanItems, Student
)

@admin.register(JobTitle)
class JobTitleAdmin(admin.ModelAdmin):
    list_display = ('title', 'code', 'is_canonical')
    search_fields = ('title', 'code')

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('name', 'job_title', 'job_number', 'email')
    search_fields = ('name', 'job_number', 'email')
    list_filter = ('nationality', 'job_title')

@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'code')
    list_editable = ('is_active',)

@admin.register(StrategicGoal)
class StrategicGoalAdmin(admin.ModelAdmin):
    list_display = ('goal_no', 'title', 'academic_year')
    list_filter = ('academic_year',)

@admin.register(OperationalGoal)
class OperationalGoalAdmin(admin.ModelAdmin):
    list_display = ('indicator_no', 'title', 'strategic_goal')
    list_filter = ('strategic_goal__academic_year',)

@admin.register(OperationalPlanItems)
class OperationalPlanItemsAdmin(admin.ModelAdmin):
    list_display = ('code', 'rank_name', 'status', 'executor_committee')
    list_filter = ('status', 'academic_year', 'executor_committee')
    search_fields = ('procedure', 'code')

admin.site.register(EvidenceFile)
admin.site.register(Committee)
admin.site.register(EvidenceDocument)
admin.site.register(Student)