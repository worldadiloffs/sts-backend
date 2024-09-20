# models.py
from django.db import models
import requests
from django.utils.translation import gettext_lazy as _
from datetime import timedelta , datetime


class Employee(models.Model):
    telegram_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    familya = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=15, unique=True)  # Telefon raqami
    status = models.BooleanField(default=False, blank=True)
    xodim_rasmi = models.ImageField(upload_to='employee_images/', blank=True, null=True)  # Xodim rasmi
    ish_joyi = models.CharField(max_length=100, blank=True, null=True)  # Ish joyi

    def __str__(self):
        return self.name

class Attendance(models.Model): # Xodimning ID raqami (Telegram ID qilingan)
    kun = models.DateField(auto_now_add=True, blank=True, verbose_name=_("Kun"))  # Ish qilingan kuni
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name=_("xodim"))
    check_in = models.CharField( max_length=10, null=True, blank=True, verbose_name=_("kelgan vaqt"))
    check_out = models.CharField(max_length=10, null=True, blank=True, verbose_name=_("ketgan vaqt"))
    latitude = models.FloatField(null=True, blank=True, editable=False)
    longitude = models.FloatField(null=True, blank=True, editable=False)
    endlatitude = models.FloatField(null=True, blank=True, editable=False)
    endlongitude = models.FloatField(null=True, blank=True, editable=False)  # Sabab saqlanadigan maydonni o'rganish uchun
    reason_for_absence = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("xodim xabari"))  # Sabab saqlanadigan maydon

    @property
    def worked_time(self):
        if self.check_in and self.check_out:  # Bo'lmasa bo'lmaydi
            check_in = str(self.check_in)
            check_out = str(self.check_out)
            start_time = datetime.strptime(check_in, '%H:%M').time()  # 08:30
            end_time = datetime.strptime(check_out, '%H:%M').time() 
            today = datetime.today()
            start_datetime = datetime.combine(today, start_time)
            end_datetime = datetime.combine(today, end_time)

            # Vaqtlar orasidagi farqni hisoblash
            time_difference = end_datetime - start_datetime

            # Oraliqni soatlarda hisoblash
            hours_difference = time_difference.total_seconds() / 3600 
            return f"{hours_difference:.2f}"
        return 0
       
    def __str__(self):
        return f'{self.employee.name} - {self.check_in} to {self.check_out}'
    

    def kelgan_manzili(self):
        if self.latitude and self.longitude:  # Maydon saqlanmagan bo'lsa bo'lmaydi
            res = requests.get(f'https://geocode.maps.co/reverse?lat={self.latitude}&lon={self.longitude}&api_key=66edb9d13db05154267785msr9f18cf')
            if res.status_code == 200:
                return res.json()['display_name']
            return "Maydon saqlanmagan"
        return ""

    def ketgan_manzil(self):
        if self.endlatitude and self.endlongitude:  # Maydon saqlanmagan bo'lsa bo'lmaydi
            res = requests.get(f'https://geocode.maps.co/reverse?lat={self.endlatitude}&lon={self.endlongitude}&api_key=66edb9d13db05154267785msr9f18cf')
            if res.status_code == 200:
                return res.json()['display_name']
            else:
                return "Maydon saqlanmagan"
        return ""

        
