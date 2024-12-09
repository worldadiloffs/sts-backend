import requests
from django.core.cache import cache
from extensions.code_generator import otp_generator, get_client_ip
from rest_framework import status
from rest_framework.response import Response
from django.conf import settings
import json



def eskiz_token():
    import requests
    req = requests.post('https://notify.eskiz.uz/api/auth/login', data = {'email': 'azamatsabina1796@mail.ru', 'password': 'AAoWE9juaZ4CirQv2Oyr06yVrloyX5o7oVgZ6Zu8'})
    response = req.json()
    token = response['data']['token']
    json_data = {
        "SMS_TOKEN": token
    }

    with open("settings.json", "w") as file:
        json.dump(json_data, file, indent=4)
    

def eskiz_token_read():
    with open('settings.json') as f:
        data = json.load(f)
        SMS_TOKEN = data['SMS_TOKEN']
        return SMS_TOKEN
    

def send_sms_otp(phone, otp):
    sms_token = eskiz_token_read()
    url = f'http://notify.eskiz.uz/api/message/sms/send?mobile_phone={phone}&from=4546&message=sts-hik.uz kirish uchun parol:{otp} ) '
    headers = {'Authorization': f'Bearer {sms_token}'}
    response = requests.post(url, headers=headers)
    return response.status_code
        


# send otp code 
def send_otp(request, phone):
    otp = otp_generator()
 
    ip = get_client_ip(request)
    # user_otp.otp = otp
    cache.set(f"{ip}-for-authentication", phone, settings.EXPIRY_TIME_OTP)
    cache.set(phone, otp, settings.EXPIRY_TIME_OTP)
    # send sms code

    response = send_sms_otp(phone, otp)
    if int(response) == 200:
        print("token ishlayapti")
        return Response(
            {
                "status": response,
                "errors": False,
                "message": "success",
            },
            status=status.HTTP_200_OK,
        )
    else:
        token_update = eskiz_token()
        print("token update bo'ldi ")
        response = send_sms_otp(phone, otp)
        if int(response) == 200:
            return Response(
                {
                    "status": response,
                    "errors": True,
                    "message": "success",
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "status": response,
                "errors": True,
                "message": "error",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )    

