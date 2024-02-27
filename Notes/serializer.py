from rest_framework import serializers
from .models import Notes
from .models import Labels
from .models import Collaborator


class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ('id', 'title', 'description', 'color', 'is_archive', 'is_trash', 'remainder', 'user')
        read_only_fields = ['is_archive', 'is_trash']
    
class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Labels
        fields = ['id','name','user']
        
class CollaboratorSerializer(serializers.ModelSerializer):
    collaborator = serializers.ListField(child=serializers.IntegerField()) 
    class Meta:
        model = Collaborator
        fields = ('id', 'access_type', 'note', 'collaborator')
        
        
    def create(self, validated_data):
        collab_user = [Collaborator(note=validated_data['note'], user_id=collab, access_type=validated_data['access_type']) for collab in validated_data['collaborator']]
        Collaborator.objects.bulk_create(collab_user)
        return Collaborator