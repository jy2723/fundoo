from django.urls import path
from . import views

urlpatterns = [
    path('', views.CreateAPI.as_view()),
    path('retrive',views.CreateAPI.as_view()),
    path('update',views.CreateAPI.as_view()),
    path('delete',views.CreateAPI.as_view())
]
