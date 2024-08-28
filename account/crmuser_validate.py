from rest_framework.views import APIView
from django.http import JsonResponse
from account.models import User
from config.settings import CRM_KEY 


class UserCrmUserApiview(APIView):
    def get(self, request, phone):
        Authorization = self.request.headers.get('Authorization')
        key = self.request.headers.get("X-Client-Key")
        if phone and (CRM_KEY==key):
            user = User.objects.filter(phone=phone).exists()
            if not user:
                user = User.objects.create(phone=phone,website_user=True)
                user.save()
                return JsonResponse({"status": "success", "errors": False, "message": "User created successfully."}, status=200)
            user_web = User.objects.filter(phone=phone).first()
            user_web.crm_user = True
            return JsonResponse({"status": "success", "errors": False, "message": "User already exists."}, status=200)
        return JsonResponse({"status": "success", "errors": True, "message": "phone, or crm key errors"}, safe=False)
          




