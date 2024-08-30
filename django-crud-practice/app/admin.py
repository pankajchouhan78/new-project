from django.contrib import admin

from .models import Employee, Subjects, Teacher, student

# Register your models here.

# class EmployeeAdmin(admin.ModelAdmin):
# list_display = ['eid','ename','department','profile']

admin.site.register(Employee)
admin.site.register(student)
admin.site.register(Subjects)
admin.site.register(Teacher)
