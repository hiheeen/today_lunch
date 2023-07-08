from rest_framework.views import APIView 
from rest_framework.response import Response
import os
from .models import Place
from users.models import User
from .serializers import PlaceSerializer
from django.shortcuts import render,redirect
import requests
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class TestPage(APIView):
    def get(self,request):
        places = Place.objects.all()
        users = User.objects.all()
        return render(request,'testpage.html',{'places':places,'users':users})

class AllPlaces(APIView):
    def get(self,request):
        places = Place.objects.all().order_by('title')
        serializer = PlaceSerializer(places,many=True)
        return Response(serializer.data)


class DeletePlace(APIView):    
    def delete(self,request,place_id):
        permission_classes = (IsAuthenticated,)
        place = Place.objects.get(id=place_id)
        if (place.user == request.user) or (request.user.id == 1):
            place.delete()
            return Response('delete completes')
        else:
            raise PermissionError
    
class CreatePlace(APIView):
    def post(self,request):
        # permission_classes = (IsAuthenticated,)
        title = request.data['title'] # 상호명
        user = User.objects.get(id=1) # 테스트용
        serializer = PlaceSerializer(data=request.data)
        print(request.data) # 테스트
        if serializer.is_valid():
            if not Place.objects.filter(title=title).exists(): # 상호명 중복 방지
                # serializer.save(user=request.user) # 원래 코드
                serializer.save(user=user) # 테스트용 # 로그인기능 구현 전까지 사용 후 환원 필요
                return Response('hh')
        return Response(serializer.errors)
    
class SearchPlace(APIView):
    def post(sel,request):
        print(request.data['place'])
        client_id = os.environ.get('NAVER_CLIENT_ID')
        client_secret = os.environ.get('NAVER_CLIENT_SECRET')
        headers = {'X-Naver-Client-Id':client_id,'X-Naver-Client-Secret':client_secret}
        try:
            kw = request.data['place'].replace(' ','')  + '신사'    

            place_search_url = 'https://openapi.naver.com/v1/search/local.json?query='
            place_url = place_search_url + kw + '$&display=1'
            place_result = requests.get(place_url,headers = headers).json()

            place_result_none_b = place_result['items'][0]['title'].replace('<b>', '').replace('</b>', '')
            
            place_result['items'][0]['title'] = place_result_none_b

            place_image_url = 'https://openapi.naver.com/v1/search/image?query='
            image_url = place_image_url + kw + '$&display=1'
            image_result = requests.get(image_url,headers = headers).json() 
            
            return Response({'place':place_result,"image":image_result})
        
        except:
            try:
                kw = request.data['place'].replace(' ','') + '논현'

                place_search_url = 'https://openapi.naver.com/v1/search/local.json?query='
                place_url = place_search_url + kw + '$&display=1'
                place_result = requests.get(place_url,headers = headers).json()

                place_result_none_b = place_result['items'][0]['title'].replace('<b>', '').replace('</b>', '')
                
                place_result['items'][0]['title'] = place_result_none_b

                place_image_url = 'https://openapi.naver.com/v1/search/image?query='
                image_url = place_image_url + kw + '$&display=1'
                image_result = requests.get(image_url,headers = headers).json() 
                
                return Response({'place':place_result,"image":image_result})
            except:
                return Response('검색결과가 없습니다.')
         
        
class ModifyPlace(APIView):
    def put(self,request,place_id):
        permission_classes = (IsAuthenticated,)
        place = Place.objects.get(id=place_id)
        
        if (place.user != request.user) or (request.user.id != 1):
            raise PermissionError
        
        serializer = PlaceSerializer(
            place,
            data = request.data,
            partial = True,
            context = {'request':request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response('Modify Complete!')
        else:
            return Response(serializer.errors)

class LikePlace(APIView):
    def post(self,request,place_id):
        permission_classes = (IsAuthenticated,)
        if request.user.is_authenticated:
            place = Place.objects.get(id=place_id)
            if place.hate_user.filter(id=request.user.id).exists():
                return Response('dont do that!')
            elif place.like_user.filter(id=request.user.id).exists():
                place.like_user.remove(request.user)
                return Response('i dont like it')
            else:
                place.like_user.add(request.user)
                return Response('like it')
            
    def get(self,request,place_id):
        permission_classes = (IsAuthenticated,)
        place = Place.objects.get(id=place_id)
        likes_num = place.like_user.count()
        return Response(likes_num)


class HatePlace(APIView):
    def post(self,request,place_id):
        permission_classes = (IsAuthenticated,)
        if request.user.is_authenticated:
            place = Place.objects.get(id=place_id)
            if place.like_user.filter(id=request.user.id).exists():
                return Response('dont do that!')
            elif place.hate_user.filter(id=request.user.id).exists():
                place.hate_user.remove(request.user)
                return Response('i dont hate it')
            else:
                place.hate_user.add(request.user)
                return Response('hate it')
            
    def get(self,request,place_id):
        permission_classes = (IsAuthenticated,)
        place = Place.objects.get(id=place_id)
        likes_num = place.hate_user.count()
        return Response(likes_num)           