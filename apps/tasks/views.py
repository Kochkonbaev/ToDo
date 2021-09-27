from rest_framework import serializers, status, views, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.tasks.models import Task
from apps.tasks.serializers import TaskSerializer
from rest_framework.generics import get_object_or_404



class TaskCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        '''
        Функция для сохранения нынешнего пользователя владельцем созданного поста
        '''
        return serializer.save(owner=self.request.user)


class TaskAllGenericView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'id'


class SetFinishedTaskAPIView(APIView):

    def get(self, request, id):
        task = get_object_or_404(Task, id=id)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def post(self, request, id, format=None): # или  же эту функцию перезаписать в "def get"
        task = get_object_or_404(Task, id=id)
        if task.is_finished:
            task.is_finished = False
        else:
            task.is_finished = True
        task.save()
        serializer = TaskSerializer(instance=task)
        return Response(serializer.data)
