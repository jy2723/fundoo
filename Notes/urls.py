from django.urls import path
from . import views
from .views import LabelAPI

my_viewset = LabelAPI.as_view({
    'get': 'get',
    'post': 'post',
    'put': 'put',
    'delete': 'delete'
})

archive = views.ArchiveTrashAPI.as_view({
    'patch': 'update_archive',
    'get': 'get_archived_notes'    
})

trash = views.ArchiveTrashAPI.as_view({
    'patch': 'update_trash',    
    'get': 'get_trash_notes'
})


urlpatterns = [
    path('', views.CreateAPI.as_view()),
    path('retrive',views.CreateAPI.as_view()),
    path('update',views.CreateAPI.as_view()),
    path('delete',views.CreateAPI.as_view()),
    path('label', my_viewset, name = 'LabelApi'),
    path('archive', archive),
    path('trash', trash),
    path('getone',views.GetoneAPI.as_view()),
    path('collaborator',views.CollaboratorAPI.as_view())
]