# admin.py
from django.contrib import admin
from .models import Employee, Attendance

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'telegram_id',)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee','kun', 'check_in', 'check_out', 'kelgan_manzili', 'ketgan_manzil', 'reason_for_absence','worked_time',)
