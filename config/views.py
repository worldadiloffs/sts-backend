from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class VersionControlView(APIView):
    def get(self, request):
        return Response({"ios": {"version": None, "link": ""}, "android": {"version": None, "link": ""}}, status=status.HTTP_200_OK) 