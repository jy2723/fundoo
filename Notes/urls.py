from django.urls import path
from . import views
from .views import LabelAPI
from .views import CreateAPI

my_viewset = LabelAPI.as_view({
    'get': 'get',
    'post': 'post',
    'put': 'put',
    'delete': 'delete'
})

viewset = CreateAPI.as_view({
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
    path('notes',viewset,name= 'CreateAPI'),
    path('label', my_viewset, name = 'LabelApi'),
    path('archive', archive),
    path('trash', trash),
    path('getone',views.GetoneAPI.as_view()),
    path('collaborator',views.CollaboratorAPI.as_view())
]