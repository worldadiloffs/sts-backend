# admin.py
from django.contrib import admin
from .models import Employee, Attendance

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    search_fields = ('name', 'telegram_id','phone_number',)
    list_display = ('name', 'telegram_id','status', 'ish_joyi',)
    list_editable = ('status',)
    # readonly_fields = ('phone_number', 'xodim_rasmi', 'ish_joyi',)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    search_fields = ('employee__phone_number', 'employee__name','kelgan_manzili',)
    list_filter = ('kun', 'employee__name', 'employee__status',)
    list_display = ('employee','kun', 'check_in', 'check_out', 'kelgan_manzili', 'ketgan_manzil', 'reason_for_absence','worked_time',)
    readonly_fields = ('latitude', 'longitude', 'endlatitude', 'endlongitude','kun',)
    list_editable = ('check_in', 'check_out',)