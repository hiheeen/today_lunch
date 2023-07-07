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
    def post(self,request):
        if not User.objects.filter(userId=request.data['userId']).exists():
            user = User.objects.create_user(
                username = request.data['username'],
                email = None,
                password = request.data['password'],
                userId = request.data['userId']
                )
            return Response('good')
        else:
            return Response('이미 존재하는 아이디입니다.')
    
# class UserLogin(APIView): # 로그인
#     def post(self,request):