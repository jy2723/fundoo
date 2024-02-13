from django.urls import path
from . import views

urlpatterns = [
    path('register_user/', views.register_user),
    path('login/',views.login)

]
