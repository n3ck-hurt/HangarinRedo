from django.contrib import admin

from .models import College, OrgMember, Organization, Program, Student


@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ('college_name', 'created_at', 'updated_at')
    search_fields = ('college_name',)
    list_filter = ('created_at',)


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('prog_name', 'college')
    search_fields = ('prog_name', 'college__college_name')
    list_filter = ('college',)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'college', 'price', 'description')
    search_fields = ('name', 'description')
    list_filter = ('college',)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'lastname', 'firstname', 'middlename', 'program')
    search_fields = ('lastname', 'firstname', 'student_id')


@admin.register(OrgMember)
class OrgMemberAdmin(admin.ModelAdmin):
    list_display = ('student', 'get_customer_caliber', 'organization', 'date_joined')
    search_fields = ('student__lastname', 'student__firstname')

    @admin.display(description='Caliber')
    def get_customer_caliber(self, obj):
        return obj.student.program if obj.student else None
