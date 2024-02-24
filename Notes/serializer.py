from rest_framework import serializers
from .models import Notes
from .models import Labels

class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ('id', 'title', 'description', 'color', 'is_archive', 'is_trash', 'remainder', 'user')
        read_only_fields = ['is_archive', 'is_trash']
    
class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Labels
        fields = ['id','name','user']