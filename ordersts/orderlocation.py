import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from extensions.code_generator import get_client_ip

# def get_client_ip(request):
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[0]  # Birinchi IP manzil asl foydalanuvchi IPsi bo'ladi
#     else:
#         ip = request.META.get('REMOTE_ADDR')
#     return ip

class LocationAPIView(APIView):
    def get(self, request):
        # Fetching location data from an external API
        # Here we use a dummy API for demonstration purposes
     # For real-world application, you'd use an external API like IP Geolocation API or MaxMind GeoIP API
        client_ip = get_client_ip(request)
        # client_ip = "213.230.120.73"
        # Replace this with your actual API request
        url =f"http://ipinfo.io/{client_ip}/geo"

        api_response = requests.get(url=url)
        data = api_response.json()
        if data:
            location_data = {
                "city": data.get("city", ""),
                "country": data.get("country_name", ""),
                "latitude": data.get("latitude", ""),
                "longitude": data.get("longitude", "")
            }
            return Response(location_data)
        else:
            return Response({"error": "Failed to retrieve location data"}, status=500)
       