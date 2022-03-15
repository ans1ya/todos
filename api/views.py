from django.shortcuts import render
from rest_framework.views import APIView
from api.models import Todos
from api.serializers import TodoSerializer,UsercreationSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics,mixins,viewsets
from django.contrib.auth.models import User
from rest_framework import authentication,permissions
from rest_framework.decorators import action


# Create your views here.
class TodosView(APIView):
    def get(self,request,*args,**kwargs):
        qs=Todos.objects.all()
        serializer=TodoSerializer(qs,many=True)
        return Response(serializer.data)
    def post(self,request,*args,**kwargs):
        serializer=TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class TodoDetails(APIView):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('id')
        qs=Todos.objects.get(id=id)
        serializer=TodoSerializer(qs)
        return Response(serializer.data)
    def put(self,request,*args,**kwargs):
        id=kwargs.get('id')
        qs=Todos.objects.get(id=id)
        serializer=TodoSerializer(instance=qs,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,*args,**kwargs):
        id=kwargs.get('id')
        qs=Todos.objects.get(id=id)
        qs.delete()
        return Response({'message':'deleted'},status=status.HTTP_200_OK)

    def patch(self,request,*args,**kwargs):
        # id=kwargs.get('id')
        qs=Todos.objects.filter(user='hana')
        serializer=TodoSerializer(instance=qs,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class TodosMixinView(generics.GenericAPIView,
                     mixins.ListModelMixin,mixins.CreateModelMixin):
    queryset = Todos.objects.all()
    serializer_class = TodoSerializer
    model=Todos
    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

class TodosDetailMixin(generics.GenericAPIView,
                       mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin):
    queryset = Todos.objects.all()
    serializer_class = TodoSerializer
    model=Todos
    lookup_field = 'id'
    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)

    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message':'deleted'},status=status.HTTP_204_NO_CONTENT)
    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)


class UsercreationView(generics.GenericAPIView,mixins.CreateModelMixin):
    serializer_class = UsercreationSerializer
    queryset = User.objects.all()
    model=User
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)


class TodosViewset(viewsets.ViewSet):
    model=Todos
    serializer_class=TodoSerializer
    def list(self,request):
        qs=Todos.objects.all()
        serializer=TodoSerializer(qs,many=True)
        return Response(serializer.data)
    def create(self,request):
        serializer=TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self,request,pk=None):
        qs = Todos.objects.get(id=pk)
        serializer = TodoSerializer(qs)
        return Response(serializer.data)

    def update(self,request,pk=None):
        qs = Todos.objects.get(id=pk)
        serializer = TodoSerializer(instance=qs, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self,request,pk=None):
        qs = Todos.objects.get(id=pk)
        qs.delete()
        return Response({'message': 'deleted'}, status=status.HTTP_200_OK)

class TodosModelViewset(viewsets.ModelViewSet):
    model=Todos
    serializer_class=TodoSerializer
    queryset = Todos.objects.all()
    authentication_classes = [authentication.SessionAuthentication,authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def create(self, request, *args, **kwargs):
        serializer=TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        qs=Todos.objects.filter(user=request.user)
        serializer=TodoSerializer(qs,many=True)
        return Response(serializer.data)
    
    @action(methods=['GET',],detail=False)
    def completed_todos(self,request,*args,**kwargs):
        qs=Todos.objects.filter(completed_status=True,user=request.user)
        serializer = TodoSerializer(qs, many=True)
        return Response(serializer.data)

    @action(methods=['GET', ], detail=False)
    def pending_todos(self,request,*args,**kwargs):
        qs = Todos.objects.filter(completed_status=False, user=request.user)
        serializer = TodoSerializer(qs, many=True)
        return Response(serializer.data)








