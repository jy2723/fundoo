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

                
class LabelAPI(viewsets.ViewSet):
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
        
        

            