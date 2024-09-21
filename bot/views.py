# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Employee, Attendance
from django.utils import timezone
from datetime import datetime , date
from django.utils import timezone


@api_view(['POST'])
def attendance(request):
    telegram_id = request.data.get('telegram_id')
    action = request.data.get('action')
    time_str = request.data.get('time')  # Botdan yuborilgan vaqt
    latitude = request.data.get('latitude')  # Lokatsiya kengligi
    longitude = request.data.get('longitude')  # Lokatsiya uzunligi
    now = timezone.now()
    time = datetime.strptime('%H:%M')
    time_str = time 
    if action == 'register':
        name = request.data.get('name')
        phone_number = request.data.get('phone_number')
        if not(Employee.objects.filter(telegram_id=telegram_id).exists()):
            employee, created = Employee.objects.get_or_create(
                telegram_id=telegram_id, 
                defaults={'name': name, 'phone_number': phone_number}
            )
            return Response({"message": "Xodim muvaffaqiyatli ro'yxatdan o'tdi Endi siz administrator tomonidan tasdiqlangan bo'lishingiz kerak"}, status=200)
        employee = Employee.objects.get(telegram_id=telegram_id)
        if not(employee.status):
            return Response({"message": "Sizning ro'yhatga o'tganingiz, admin ruxsat berishi  kerak"}, status=400)

    try:
        employee = Employee.objects.get(telegram_id=telegram_id)
        if employee.phone_number is None:
            return Response({"message": "Sizning telefon raqamini yuborishni shoqlayman"}, status=400)
        if not(employee.status):
            return Response({"message": "Sizning ro'yhatga o'tganingiz, admin ruxsat berishi  kerak"}, status=200)
    except Employee.DoesNotExist:
        return Response({"message": "Siz ro'yhatdan o'tmagansiz"}, status=404)

    try:
        if time_str is not None:
            # time_obj = datetime.strptime(time_str, '%H:%M')  # Vaqtni to'g'ri formatda parse qilish
            if action == 'check_in':
                if not(Attendance.objects.filter(employee=employee, kun=date.today()).exists()):
                    if not(employee.status):
                        return Response({"message": "Sizni admin tasdiqlamagan"}, status=400)
                    attendance = Attendance.objects.create(employee=employee, kun=date.today())
                    # attendance, created = Attendance.objects.get_or_create(employee=employee, check_out=None)
                    attendance.check_in = time_str
                    attendance.latitude = latitude
                    attendance.longitude = longitude
                    attendance.save()
                    return Response({"message": "Roʻyxatdan oʻtish muvaffaqiyatli qayd etildi"}, status=200)
                else:
                    return Response({"message": "Siz allaqachon vaqti yoki sababni belgilangiz"}, status=400)

            elif action == 'check_out':
                try:
                    if Attendance.objects.filter(employee=employee, kun=date.today()).exists():
                        attendance = Attendance.objects.get(employee=employee, kun=date.today())
                        if not(employee.status):
                            return Response({"message": "Sizni admin tasdiqlamagan"}, status=400)
                        if attendance.check_in is not None and attendance.check_out is None:
                            attendance.check_out = time_str
                            attendance.endlatitude = latitude
                            attendance.endlongitude = longitude
                            attendance.save()
                            times_work = attendance.worked_time
                            return Response({"message": "Ketish vaqtingiz  muvaffaqiyatli qayd etildi" ,"time":times_work}, status=200)
                        if attendance.check_out is not None:
                            return Response({"message": f"Siz ketgan vaqtingiz {attendance.check_out}"}, status=400)
                        return Response({"message": "Siz kelgan vaqtingizni belgilamagansiz"}, status=400)
                    return Response({"message": "Siz kelgan vaqti belgilamagansiz"}, status=400)
                except Attendance.DoesNotExist:
                    return Response({"message": "Check-in record not found"}, status=404)
            
        if action == 'absence':
            reason = request.data.get('reason')
            if not(employee.status):
                    return Response({"message": "Sizni admin tasdiqlamagan"}, status=400)
            if not(Attendance.objects.filter(employee=employee, kun=date.today()).exists()):
                attendance = Attendance.objects.create(employee=employee, kun=date.today())
                attendance.reason_for_absence = reason
                attendance.save()
                return Response({"message": "Sabab saqlanadigan maydonni muvaffaqiyatli qayd etildi"}, status=200)
            attendance = Attendance.objects.get(employee=employee, kun=date.today())
            return Response({"message": f"Yo'qlik sababi qayd etilgan: {attendance.reason_for_absence}"}, status=400)
    
    except ValueError:
        return Response({"message": "Invalid time format"}, status=400)

    return Response({"message": "Registratsiya qilingan"}, status=400)
