from django.urls import path
from . import views

urlpatterns = [
    path('create_user/',views.CreateUser.as_view()),
    path('',views.TestPage.as_view()),
]
