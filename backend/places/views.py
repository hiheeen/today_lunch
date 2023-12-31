from rest_framework.views import APIView 
from rest_framework.response import Response
import os
from .models import Place
from .serializers import PlaceSerializer
from django.shortcuts import render,redirect
import requests
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class AllPlaces(APIView):
    def get(self,request):
        places = Place.objects.all().order_by('title')
        serializer = PlaceSerializer(places,many=True)
        
        return Response(serializer.data,status = status.HTTP_202_ACCEPTED) 

class DeletePlace(APIView):    
    def delete(self,request,place_id):
        permission_classes = (IsAuthenticated,)
        place = Place.objects.get(id=place_id)
        print('가나단아낭ㄴ',request.user)
        print('place user : ',place.user)
        if (place.user == request.user) or (request.user.id == 1):
            place.delete()
            return Response(status = status.HTTP_200_OK)
        else:
            raise PermissionError
    
class CreatePlace(APIView):
    def post(self,request):
        # permission_classes = (IsAuthenticated,)
        title = request.data['title'] # 상호명
        serializer = PlaceSerializer(data=request.data)
        if serializer.is_valid():
            if not Place.objects.filter(title=title).exists(): # 상호명 중복 방지
                serializer.save(user=request.user) # 원래 코드
                # serializer.save(user=user) # 테스트용 # 로그인기능 구현 전까지 사용 후 환원 필요
                return Response('hh')
        return Response(serializer.errors)
    
class SearchPlace(APIView):
    def post(self,request):
        try:
            kw = request.data['place'].replace(' ','')  + '신사'    

            place_search_url = os.environ.get('NAVER_SEARCH_URL')
            place_url = place_search_url + kw 
            search_result = requests.get(place_url).json()
            
            category = ">".join(search_result['result']['place']['list'][0]['category'])

            result = {
                "place" : {
                    "items" : [{
                        "title" : search_result['result']['place']['list'][0]['name'],
                        "category" : category,
                        "mapx" : search_result['result']['place']['list'][0]['x'],
                        "mapy" : search_result['result']['place']['list'][0]['y']
                    }]
                },
                "image" : {
                    "items" : [{
                        "link" : search_result['result']['place']['list'][0]['thumUrl']
                    }]
                }
            }

            return Response(result,status = status.HTTP_200_OK)
        
        except:
            return Response(status = status.HTTP_204_NO_CONTENT)
            
# class SearchPlace(APIView):
#     def post(sel,request):
#         client_id = os.environ.get('NAVER_CLIENT_ID')
#         client_secret = os.environ.get('NAVER_CLIENT_SECRET')
#         headers = {'X-Naver-Client-Id':client_id,'X-Naver-Client-Secret':client_secret}
#         try:
#             kw = request.data['place'].replace(' ','')  + '신사'    

#             place_search_url = 'https://openapi.naver.com/v1/search/local.json?query='
#             place_url = place_search_url + kw + '$&display=1'
#             place_result = requests.get(place_url,headers = headers).json()

#             place_result_none_b = place_result['items'][0]['title'].replace('<b>', '').replace('</b>', '')
            
#             place_result['items'][0]['title'] = place_result_none_b

#             place_image_url = 'https://openapi.naver.com/v1/search/image?query='
#             image_url = place_image_url + kw + '$&display=1'
#             image_result = requests.get(image_url,headers = headers).json() 
            
#             return Response({'place':place_result,"image":image_result},status = status.HTTP_200_OK)
        
#         except:
#             try:
#                 kw = request.data['place'].replace(' ','') + '논현'

#                 place_search_url = 'https://openapi.naver.com/v1/search/local.json?query='
#                 place_url = place_search_url + kw + '$&display=1'
#                 place_result = requests.get(place_url,headers = headers).json()

#                 place_result_none_b = place_result['items'][0]['title'].replace('<b>', '').replace('</b>', '')
                
#                 place_result['items'][0]['title'] = place_result_none_b

#                 place_image_url = 'https://openapi.naver.com/v1/search/image?query='
#                 image_url = place_image_url + kw + '$&display=1'
#                 image_result = requests.get(image_url,headers = headers).json() 
                
#                 return Response({'place':place_result,"image":image_result},status = status.HTTP_200_OK)
#             except:
#                 return Response(status = status.HTTP_204_NO_CONTENT)
         
class ModifyPlace(APIView):
    def put(self,request,place_id):
        # permission_classes = (IsAuthenticated,)
        place = Place.objects.get(id=place_id)
        print(request.user)
        if (place.user == request.user) or (request.user.id == 1):
        
            serializer = PlaceSerializer(
                place,
                data = request.data,
                partial = True,
                context = {'request':request}
            )

            if serializer.is_valid():
                serializer.save()
                return Response(status = status.HTTP_202_ACCEPTED)
            else:
                return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        else:
            raise PermissionError

class LikePlace(APIView):
    def post(self,request,place_id):
        print('랄라', request.user)
        permission_classes = (IsAuthenticated,)
        place = Place.objects.get(id=place_id)
        if place.hate_user.filter(id=request.user.id).exists():
            return Response(status = status.HTTP_400_BAD_REQUEST)
        elif place.like_user.filter(id=request.user.id).exists():
            place.like_user.remove(request.user)
            return Response(status = status.HTTP_202_ACCEPTED)
        else:
            place.like_user.add(request.user)
            return Response(status = status.HTTP_202_ACCEPTED)

class HatePlace(APIView):
    def post(self,request,place_id):
        permission_classes = (IsAuthenticated,)
        place = Place.objects.get(id=place_id)
        if place.like_user.filter(id=request.user.id).exists():
            return Response(status = status.HTTP_400_BAD_REQUEST)
        elif place.hate_user.filter(id=request.user.id).exists():
            place.hate_user.remove(request.user)
            return Response(status = status.HTTP_202_ACCEPTED)
        else:
            place.hate_user.add(request.user)
            return Response(status = status.HTTP_202_ACCEPTED)