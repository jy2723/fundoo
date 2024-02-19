from rest_framework.views import APIView
from .serializer import NotesSerializer
from rest_framework.response import Response
from .models import Notes

class CreateAPI(APIView):
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
        
            if notes is None:
                return Response({'message': 'No notes with this id', 'status': 400}, status=400)
            
            
            serializer = NotesSerializer(notes,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'message': 'note updated', 'status': 201, 
                            'data': serializer.data}, status=201)
        except Exception as e:
            return Response({'message': str(e), 'status': 400}, status=400)
    
    def delete(self,request):
        try:
            user_id = request.data.get('id')
            notes = Notes.objects.get(id=user_id)
            if notes is None:
                return Response({'message': 'No notes with this id', 'status': 400}, status=400)
            notes.delete() 
            return Response({'message': 'note deleted', 'status': 201, 
                            }, status=201)
            
        except Exception as e:
            return Response({'message': str(e), 'status': 400}, status=400)
        

            