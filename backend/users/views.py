from django.shortcuts import redirect,render
from rest_framework.views import APIView 
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from django.contrib.auth.models import UserManager

class TestPage(APIView):
    def get(self,request):
        users = User.objects.all()
        return render(request,'createuser.html',{'users':users})

class CreateUser(APIView):
    def post(self,request): # 회원가입 아이디 중복확인 필요
        user = User.objects.create_user(
            username = request.data['username'],
            email = None,
            password = request.data['password'],
            userId = request.data['userId']
            )
        # return Response('Hi')
        return redirect('api/v1/users')
    
# class UserLogin(APIView): # 로그인
#     def post(self,request):
