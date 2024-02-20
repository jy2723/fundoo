from rest_framework.views import APIView
from .serializer import NotesSerializer
from rest_framework.response import Response
from .models import Notes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializer import LabelSerializer
from .models import Labels
from rest_framework import viewsets


class CreateAPI(APIView):
    
    authentication_classes =(JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def post(self,request):
        try:
            serializer = NotesSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'message': 'note created', 'status': 201, 
                            'data': serializer.data}, status=201)
        except Exception as e:
            return Response({'message': str(e), 'status': 400}, status=400)
    
    def get(self,request):
        try:
            user_id = request.data.get('id')
            notes = Notes.objects.filter(user_id=user_id)
            serializer = NotesSerializer(notes, many=True)
            return Response({'message':'succusfully fetched data','status': 201,'data':serializer.data},status=201)
        except Exception as e:
            return Response({'message': str(e), 'status': 400}, status=400)
        
    def put(self,request):
        try:
            user_id = request.data.get('id')
            notes = Notes.objects.get(user_id=user_id)
        
            
            serializer = NotesSerializer(notes,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'message': 'note updated', 'status': 201, 
                            'data': serializer.data}, status=201)
            
        except Notes.DoesNotExist:
            return Response({'message': 'notes not found', 'status': 400},status = 404)
        except Exception as e:
            return Response({'message': str(e), 'status': 400}, status=400)
    
    def delete(self,request):
        try:
            user_id = request.data.get('id')
            notes = Notes.objects.get(id=user_id)
            notes.delete() 
            return Response({'message': 'note deleted', 'status': 201, 
                            }, status=201)
        
        except Notes.DoesNotExist:
            return Response({'message': 'notes not found', 'status':404},status = 404)
        
        except Exception as e:
            return Response({'message': str(e), 'status': 400}, status=400)


class ArchiveTrashAPI(viewsets.ViewSet):        
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def update_archive(self, request):
        try:
            note_id = request.query_params.get('note_id')
            if not note_id:
                return Response({"msg": "Note ID not found", "status": 404}, status=404)
            note = Notes.objects.get(id=note_id, user=request.user)
            note.is_archive = True if not note.is_archive else False
            note.save()
            if note.is_archive:
                return Response({'message': 'Note moved to Archive', 'status':200}, status=200)
            return Response({'message': 'Note moved out of Archive', 'status': 200}, status=200)
        except Notes.DoesNotExist:
            return Response({'message': 'Note does not Exist', 'status': 404}, status=404)
        except Exception as e:
            return Response({'message': str(e), 'status': 400}, status=400)

    def get_archived_notes(self, request):
        try:
            notes = Notes.objects.filter(user=request.user, is_archive=True, is_trash=False)
            serializer = NotesSerializer(notes, many=True)
            return Response({'message': 'Archived Notes', 'status': 200, 'Data': serializer.data}, status=200)
        except Notes.DoesNotExist:
            return Response({'message': 'Note does not Exist', 'status': 404}, status=404)
        except Exception as e:
            return Response({'message': str(e), 'status': 400}, status=400)

    def update_trash(self, request):
        try:
            note_id = request.query_params.get('note_id')
            if not note_id:
                return Response({"msg": "Note ID not found", "status": 404}, status=404)
            note = Notes.objects.get(id=note_id, user=request.user)
            note.is_trash = True if not note.is_trash else False
            note.save()
            if note.is_trash:
                return Response({'message': 'Note moved to Trash', 'status':200}, status=200)
            return Response({'message': 'Note moved out of Trash', 'status': 200}, status=200)
        except Notes.DoesNotExist:
            return Response({'message': 'Note does not Exist', 'status': 404}, status=404)
        except Exception as e:
            return Response({'message': str(e), 'status': 400}, status=400)

    def get_trash_notes(self, request):
        try:
            notes = Notes.objects.filter(user=request.user, is_trash=True)
            serializer = NotesSerializer(notes, many=True)
            return Response({'message': 'Trashed Notes', 'status': 200, 'Data': serializer.data}, status=200)
        except Notes.DoesNotExist:
            return Response({'message': 'Note does not Exist', 'status': 404}, status=404)
        except Exception as e:
            return Response({'message': str(e), 'status': 400}, status=400)
        
class LabelAPI(viewsets.ViewSet):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        try:
            serializer = LabelSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'message': 'label created', 'status': 201, 
                            'data': serializer.data}, status=201)
        except Exception as e:
            return Response({'message': str(e), 'status': 400}, status=400)
    
    def get(self,request):
        try:
            user_id = request.data.get('id')
            label = Labels.objects.filter(user_id=user_id)
            serializer = LabelSerializer(label, many=True)
            return Response({'message':'succusfully fetched data','status': 201,'data':serializer.data},status=201)
        except Exception as e:
            return Response({'message': str(e), 'status': 400}, status=400)
        
    def put(self,request):
        try:
            user_id = request.data.get('id')
            label = Labels.objects.get(user_id=user_id)
            serializer = LabelSerializer(label,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'message': 'label updated', 'status': 201, 
                            'data': serializer.data}, status=201)
            
        except Labels.DoesNotExist:
            return Response({'message': 'label not found', 'status': 400},status = 404)
        except Exception as e:
            return Response({'message': str(e), 'status': 400}, status=400)
        
    def delete(self,request):
        try:
            user_id = request.data.get('id')
            label = Labels.objects.get(id=user_id)
            label.delete() 
            return Response({'message': 'label deleted', 'status': 201, 
                            }, status=201)
        
        except Labels.DoesNotExist:
            return Response({'message': 'label not found', 'status':404},status = 404)
        
        except Exception as e:
            return Response({'message': str(e), 'status': 400}, status=400)
        
        

            