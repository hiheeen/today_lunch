from django.urls import path
from . import views

urlpatterns = [
    path('',views.AllPlaces.as_view()),
    path('create_place/',views.CreatePlace.as_view()),
    path('search_place/',views.SearchPlace.as_view()),
    path('delete_place/<int:place_id>/',views.DeletePlace.as_view()),
    path('modify_place/<int:place_id>/',views.ModifyPlace.as_view()),
    path('like_place/<int:place_id>/',views.LikePlace.as_view()),
    path('hate_place/<int:place_id>/',views.HatePlace.as_view()),
]