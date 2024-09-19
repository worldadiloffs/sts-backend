from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render

class VersionControlView(APIView):
    def get(self, request):
        return Response({"ios": {"version": None, "link": ""}, "android": {"version": None, "link": ""}}, status=status.HTTP_200_OK) 
    

def check_render(request):
    return render(request, 'check.html')
    

