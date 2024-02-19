from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserAPI.as_view(), name='userApi'),
    path('login/', views.AuthUserAPI.as_view(), name='login'),

]
