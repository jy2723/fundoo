from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserAPI.as_view()),
    path('login/',views.LoginAPI.as_view())

]
