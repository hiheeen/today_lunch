from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView 
from rest_framework.response import Response
from .models import User
from rest_framework.permissions import IsAuthenticated 
from rest_framework_simplejwt.tokens import RefreshToken


class TestPage(APIView):
    def get(self,request):
        users = User.objects.all()
        return render(request,'createuser.html',{'users':users})

class CreateUser(APIView):
    def post(self,request):
        if not User.objects.filter(userId=request.data['userId']).exists():
            user = User.objects.create_user(
                username = request.data['username'],
                password = request.data['password'],
                userId = request.data['userId']
                )
            return Response('good')
        else:
            return Response('이미 존재하는 아이디입니다.')
        
class Logout(APIView):
     permission_classes = (IsAuthenticated,)
     def post(self, request):
          try:
               refresh_token = request.data["refresh_token"]
               token = RefreshToken(refresh_token)
               token.blacklist()
               return Response(status=status.HTTP_205_RESET_CONTENT)
          except Exception as e:
               return Response(status=status.HTTP_400_BAD_REQUEST)
    
# class UserLogin(APIView): # 로그인
#     def post(self,request):