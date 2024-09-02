import requests
SMS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3Mjc4NjMzNTMsImlhdCI6MTcyNTI3MTM1Mywicm9sZSI6InVzZXIiLCJzaWduIjoiY2Y0N2M0NzdmYmE2OWMxNmM4ZDllMmZmMjE5MDFhNzg3N2NkYmNmYTVkM2FiZGI3NjU4ZTVhYjgxZjk2MThjOCIsInN1YiI6IjgyOCJ9.SaAwjpKEg2n5Z3y8gNCZlZGBIFfnuH1M1i9h516C8wo"

url = f'http://notify.eskiz.uz/api/message/sms/send?mobile_phone=998990167647&from=4546&message=sts-hik.uz kirish uchun parol:292402)' 
headers = {'Authorization': f'Bearer {SMS_TOKEN}'}
response = requests.post(url, headers=headers)

print(response.json())
