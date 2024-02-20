from rest_framework import serializers
from .models import Notes
from .models import Labels

class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['id','title','description','color', 'user']
    
class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Labels
        fields = ['id','name','user']