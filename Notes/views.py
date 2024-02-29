from rest_framework.views import APIView
from .serializer import NotesSerializer
from rest_framework.response import Response
from .models import Notes
from user.models import User
from .models import Collaborator
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializer import LabelSerializer,CollaboratorSerializer
from .models import Labels
from rest_framework import viewsets
from .utils import Redismanager
import json
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db import connection


class CreateAPI(viewsets.ViewSet):
    
    authentication_classes =(JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    @swagger_auto_schema(
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'title': openapi.Schema(type=openapi.TYPE_STRING),
            'description': openapi.Schema(type=openapi.TYPE_STRING),
            'color': openapi.Schema(type=openapi.TYPE_STRING),
            'reminder': openapi.Schema(type=openapi.TYPE_STRING,example="YYYY-MM-DDTHH:MM:SSZ"),
        },
        required=['title', 'description', 'color', 'reminder']
    ),
    responses={
        201: openapi.Response(
            description="Note Created",
            examples={"application/json": {'message': 'Note Created', 'status': 201, 'data': {}}}
        ),
        400: "Bad Request",
        401: "Unauthorized"
    }
)

    def post(self,request):
        try:
            request.data['user'] = request.user.id
            serializer = NotesSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            note_id = serializer.instance.id
            data_json = json.dumps(serializer.data)
            Redismanager.save(f'user_{request.user.id}', f'note_{note_id}', data_json)
            return Response({'message': 'note created', 'status': 201, 
                            'data': serializer.data}, status=201)
        except Exception as e:
            return Response({'message': str(e), 'status': 400}, status=400)
    
    @swagger_auto_schema(responses={200: openapi.Response(description="Response", examples={
                             "application/json": {'message': 'Successfully Fetched Data','data':{}, 'status': 200}
                         }),
                                    400: "Bad Request", 401:"Unauthorized"})  
    def get(self, request):
        try:
            cache_notes = Redismanager.get(f'user_{request.user.id}')
            if cache_notes:
                return Response({'message': 'Successfully Fetched Data from Cache', 'status': 200, 'data': cache_notes}, status=200)
            lookup = Q(user_id=request.user.id) | Q(collaborator__user=request.user)
            notes = Notes.objects.filter(lookup)
            serializer = NotesSerializer(notes, many=True)
            return Response({'message': 'Successfully Fetched Data', 'status': 200, 'data': serializer.data}, status=200)
        except Exception as e:
            return Response({'message': str(e), 'status': 400}, status=400)
    
    @swagger_auto_schema(
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id':openapi.Schema(type=openapi.TYPE_INTEGER),
            'title': openapi.Schema(type=openapi.TYPE_STRING),
            'description': openapi.Schema(type=openapi.TYPE_STRING),
            'color': openapi.Schema(type=openapi.TYPE_STRING),
            'reminder': openapi.Schema(type=openapi.TYPE_STRING,example="YYYY-MM-DDTHH:MM:SSZ"),
        },
        required=['id','title', 'description', 'color']
    ),
    responses={
        201: openapi.Response(
            description="Note updated",
            examples={"application/json": {'message': 'Note Updated', 'status': 201, 'data': {}}}
        ),
        400: "Bad Request",
        401: "Unauthorized",
        404:"notesnot found"
    }
)
    def put(self,request):
        try:
            request.data['user'] = request.user.id
            note = request.data.get('id')
            user_id = request.data.get('user')
            notes = Notes.objects.get(id = note , user_id= user_id)
            serializer = NotesSerializer(notes,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            note_id = serializer.instance.id
            data_json = json.dumps(serializer.data)
            key = f'user_{request.user.id}'
            Redismanager.save(key,f'note_{note_id}', data_json)
            return Response({'message': 'note updated', 'status': 201, 
                            'data': serializer.data}, status=201)
            
        except Notes.DoesNotExist:
            return Response({'message': 'notes not found', 'status': 404},status = 404)
        except Exception as e:
            return Response({'message': str(e), 'status': 400}, status=400)
    
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('id', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True)], responses={200: openapi.Response(description="Response", examples={
                             "application/json": {'message': 'Successfully Deleted Data','data':{}, 'status': 200}
                         }),
                                    400: "Bad Request", 401:"Unauthorized",404:"Notes not found"})  
    def delete(self,request):
        try:
            
            note_id = request.query_params.get('id')
            notes = Notes.objects.get(id=note_id)
            notes.delete() 
            key = f'user_{request.user.id}'
            Redismanager.delete(key, f'note_{note_id}')
            return Response({'message': 'Successfully Deleted Cache Data', 'status': 200,}, status=200)

        
        except Notes.DoesNotExist:
            return Response({'message': 'notes not found', 'status':404},status = 404)
        
        except Exception as e:
            return Response({'message': str(e), 'status': 400}, status=400)

class GetoneAPI(APIView):
    authentication_classes =(JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('note_id', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True)
    ], responses={200: openapi.Response(description="Response", examples={
                             "application/json": {'message': 'Successfully Fetched Data','data':{}, 'status': 200}
                         }),
                                    400: "Bad Request", 401:"Unauthorized"})  
    def get(self,request):
        try:
            note_id = request.query_params.get('note_id')
            key = f'user_{request.user.id}'
            cache_notes = Redismanager.get_one(key, f'note_{note_id}')
            if cache_notes:
                return Response({'message': 'Successfully Fetched Data from Cache', 'status': 200, 'data': cache_notes}, status=200)
            else:
                return Response({'message': 'No data found in cache', 'status': 404}, status=404)
        except Exception as e:
            return Response({'message': str(e), 'status': 400}, status=400)
            

class ArchiveTrashAPI(viewsets.ViewSet):        
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('note_id', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True)
    ], responses={200: openapi.Response(description="Response", examples={
                             "application/json": {'message': 'Note moved to Archive', 'status': 200,'data':{}}
                         }),
                                    400: "Bad Request", 401:"Unauthorized",404:"Note ID not found"})
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

    @swagger_auto_schema(responses={200: openapi.Response(description="Response", examples={
                             "application/json": {'message': 'Archived notes', 'status': 200,'data':{}}
                         }),
                                    400: "Bad Request", 401:"Unauthorized",404:"Note does not Exist"})
    def get_archived_notes(self, request):
        try:
            notes = Notes.objects.filter(user=request.user, is_archive=True, is_trash=False)
            serializer = NotesSerializer(notes, many=True)
            return Response({'message': 'Archived Notes', 'status': 200, 'Data': serializer.data}, status=200)
        except Notes.DoesNotExist:
            return Response({'message': 'Note does not Exist', 'status': 404}, status=404)
        except Exception as e:
            return Response({'message': str(e), 'status': 400}, status=400)

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('note_id', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True)
    ], responses={200: openapi.Response(description="Response", examples={
                             "application/json": {'message': 'Note moved to Trash', 'status': 200,'data':{}}
                         }),
                                    400: "Bad Request", 401:"Unauthorized",404:"Note does not Exist"})
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

    @swagger_auto_schema(responses={200: openapi.Response(description="Response", examples={
                             "application/json": {'message': 'Trashed notes', 'status': 200,'data':{},}
                         }),
                                    400: "Bad Request", 401:"Unauthorized",404:"Note does not Exist"})
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
    
    @swagger_auto_schema(
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=['name']
    ),
    responses={
        201: openapi.Response(
            description="Note Created",
            examples={"application/json": {'message': 'label Created', 'status': 201, 'data': {}}}
        ),
        400: "Bad Request",
        401: "Unauthorized"
    }
)

    def post(self,request):
        try:
            request.data['user'] = request.user.id
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO labels (name, user_id) values (%s, %s)", (request.data['name'], request.data['user']))
                cursor.execute("select * from labels order by id desc fetch first row only")
                columns = [col[0] for col in cursor.description]
                data = cursor.fetchone() 
                data = dict(zip(columns, data))
            # request.data['user'] = request.user.id
            # serializer = LabelSerializer(data=request.data)
            # serializer.is_valid(raise_exception=True)
            # serializer.save()
            return Response({'message': 'label created', 'status': 201, 
                            'data': data}, status=201)
        except Exception as e:
            return Response({'message': str(e), 'status': 400}, status=400)
    
    @swagger_auto_schema(responses={200: openapi.Response(description="Response", examples={
                             "application/json": {'message': 'succusfully fetched data','data':{}, 'status': 200,}
                         }),
                                    400: "Bad Request", 401:"Unauthorized"})
    
    def get(self,request):
        try:
            # with connection.cursor() as cursor:
            #     query = "SELECT * FROM labels WHERE user_id = %s"
            #     cursor.execute(query, [request.user.id])
            #     columns = [col[0] for col in cursor.description]
            #     print(columns)
            #     data = [dict(zip(columns, row)) for row in cursor.fetchall()]
                
            label = Labels.objects.filter(user_id=request.user.id)
            label = Labels.objects.raw("select * from labels where user_id= %s",(request.user.id,))
            serializer = LabelSerializer(label, many=True)
            return Response({'message':'succusfully fetched data','status': 201,'data': serializer.data},status=201)
        except Exception as e:
            return Response({'message': str(e), 'status': 400}, status=400)
    
    @swagger_auto_schema(
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_INTEGER),
            'name': openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=['name']
    ),
    responses={
        201: openapi.Response(
            description="Note Created",
            examples={"application/json": {'message': 'label Created', 'status': 201, 'data': {}}}
        ),
        400: "Bad Request",
        401: "Unauthorized"
    }
)
    def put(self,request):
        try:
            # request.data['user'] = request.user.id
            # label = Labels.objects.get(id = request.data.get('id'), user_id=request.data.get('user'))
            # serializer = LabelSerializer(instance = label, data = request.data)
            # serializer.is_valid(raise_exception=True)
            # serializer.save()
            request.data['user'] = request.user.id
            name = request.data.get('name')
            with connection.cursor() as cursor:
                cursor.execute("UPDATE labels SET name = %s WHERE user_id = %s and id = %s", (name, request.data['user'],request.data.get('id')))
                cursor.execute("SELECT * FROM labels WHERE user_id = %s and id = %s", (request.data['user'],request.data.get('id')))
                columns = [col[0] for col in cursor.description]
                data = cursor.fetchone() 
                data = dict(zip(columns, data))
            return Response({'message': 'label updated', 'status': 201, 
                            'data': data}, status=201)
            
        except Labels.DoesNotExist:
            return Response({'message': 'label not found', 'status': 404},status = 404)
        except Exception as e:
            return Response({'message': str(e), 'status': 400}, status=400)
    
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('label_id', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True)
    ], responses={200: openapi.Response(description="Response", examples={
                             "application/json": {'message': 'label deleted','data':{}, 'status': 200}
                         }),
                                    400: "Bad Request", 401:"Unauthorized",404:"Label not found"})
    def delete(self,request):
        try:
            request.data['user'] = request.user.id
            label_id = request.query_params.get('label_id')
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM labels WHERE id = %s AND user_id = %s", (label_id, request.data['user']))
            # # label_id = request.query_params.get('label_id')
            # label = Labels.objects.raw("DELETE * from labels where user_id= %s and label_id= %s",(request.user.id,request.query_params.get('label_id')))
            # # label = Labels.objects.get(id=label_id)
            # label.delete() 
            return Response({'message': 'label deleted', 'status': 201, 
                            }, status=201)
        
        except Labels.DoesNotExist:
            return Response({'message': 'label not found', 'status':404},status = 404)
        
        except Exception as e:
            return Response({'message': str(e), 'status': 400}, status=400)
        
        
class CollaboratorAPI(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['note_id', 'user_ids'],
        properties={
            'note_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            'user_ids': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(type=openapi.TYPE_INTEGER)
            ),
            'access_type': openapi.Schema(type=openapi.TYPE_STRING, default='read only')
        }
    ),
    responses={
        200: openapi.Response(description="Success", examples={
            "application/json": {'message': 'Notes shared to users successfully', 'status': 200}
        }),
        400: "Bad Request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Note does not exist"
    })
    def post(self, request):
        try:
            user_id = request.user.id
            user_ids = request.data.get('user_ids',[])
            note_id = request.data.get('note_id') 
            access_type = request.data.get('access_type','read only')

            if user_id is None or note_id is None:
                return Response({'message': 'user_id and note_id must be provided','status': 400}, status=400)

            note = Notes.objects.get(id=note_id)
            
            if note.user_id != user_id:
                return Response({'message': 'You are not the owner of this note', 'status': 403}, status=403)
            
            for user_id in user_ids:
                user = User.objects.get(id=user_id)

                collaborator, created = Collaborator.objects.get_or_create(user=user, note=note, access_type=access_type)
                if created:
                    print(f"Collaborator created: {collaborator}")
                else:
                    print(f"Collaborator already exists for user {user_id} and note {note_id}")

            return Response({'message': 'Notes shared to user successfully', 'status': 200}, status=200)


        except (User.DoesNotExist, Notes.DoesNotExist):
            return Response({'message': 'User or notes does not exist','status': 400}, status=400)

        except Exception as e:
            return Response({'message': str(e), 'status': 400}, status=400)
    
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['note_id', 'user_ids'],
        properties={
            'note_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            'user_ids': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(type=openapi.TYPE_INTEGER)
            )
        }
    ),
    responses={
        200: openapi.Response(description="Success", examples={
            "application/json": {'message': 'Collaborator removed from note successfully', 'status': 200}
        }),
        400: "Bad Request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "User, Note, or Collaborator not found"
    })
    def delete(self,request):
        try:
            user_id = request.user.id
            note_id = request.data.get('note_id')
            user_ids = request.data.get('user_ids',[])

            user = User.objects.get(id=user_id)
            note = Notes.objects.get(id=note_id)
            
            if note.user_id != user_id:
                return Response({'message': 'You are not the owner of this note', 'status': 403}, status=403)
            
            for user_id in user_ids:
                try:
                    user = User.objects.get(id=user_id)
                    collaborator = Collaborator.objects.get(user=user, note=note)
                    collaborator.delete()
                    
                except collaborator.DoesNotExist:
                    return Response({"message": 'collaborator does not exist','status':400},status=400)
                
            return Response({'message': 'Collaborator removed from note successfully', 'status':200},status=200)
        
        except (User.DoesNotExist, Notes.DoesNotExist, Collaborator.DoesNotExist):
            return Response({'message': 'User, Note, or Collaborator not found','status':400}, status=400)
                
        except Exception as e:
            return Response({'message': str(e), 'status': 400}, status=400)
        
# class CollaboratorAPI(APIView):
    
#     authentication_classes = (JWTAuthentication,)
#     permission_classes = (IsAuthenticated,)
    
#     def post(self, request):
#         try:
#             request.data.update({'user_id': request.user.id})
#             serializer = CollaboratorSerializer(data=request.data)
#             serializer.is_valid(raise_exception=True)
#             serializer.save() 
#             return Response({'message': f'Note Shared to {request.data["collaborator"]}', 'status': 200}, status=200)
#         except Exception as e:
#             return Response({'message': str(e), 'status': 400}, status=400)
        
#     def delete(self, request):
#         try:
#             note_id = request.data.get('note')
#             user_id = request.user.id

#             note = Notes.objects.get(id=note_id, user_id=user_id)

#             for collaborator_id in request.data.get('collaborator', []):
#                 collaborator = User.objects.get(id=collaborator_id)
#                 note.collaborators.remove(collaborator)
#             return Response({'message': f'Removed access to user', 'status': 200}, status=200)
#         except Exception as e:
#             return Response({'message': str(e), 'status': 400}, status=400)
            