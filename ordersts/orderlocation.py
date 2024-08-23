import requests
from rest_framework.views import APIView
from rest_framework.response import Response

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # Birinchi IP manzil asl foydalanuvchi IPsi bo'ladi
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class LocationAPIView(APIView):
    def get(self, request):
        # Fetching location data from an external API
        # Here we use a dummy API for demonstration purposes
     # For real-world application, you'd use an external API like IP Geolocation API or MaxMind GeoIP API
        client_ip = get_client_ip(request)
        print(client_ip)
        client_ip = "213.230.120.73"
        # Replace this with your actual API request
        api_response = requests.get(f"http://ipinfo.io/{client_ip}/geo")
        data = api_response.json()
        if data.get("status", {}).get("code") == 200:
            location_data = {
                "city": data.get("city", ""),
                "country": data.get("country_name", ""),
                "latitude": data.get("latitude", ""),
                "longitude": data.get("longitude", "")
            }
            return Response(location_data)
        else:
            return Response({"error": "Failed to retrieve location data"}, status=500)
       