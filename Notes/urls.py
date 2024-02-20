from django.urls import path
from . import views
from .views import LabelAPI

my_viewset = LabelAPI.as_view({
    'get': 'get',
    'post': 'post',
    'put': 'put',
    'delete': 'delete'
})

urlpatterns = [
    path('', views.CreateAPI.as_view()),
    path('retrive',views.CreateAPI.as_view()),
    path('update',views.CreateAPI.as_view()),
    path('delete',views.CreateAPI.as_view()),
    path('label', my_viewset, name = 'LabelApi'),
]