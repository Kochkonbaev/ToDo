from rest_framework import serializers, status, views, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.tasks.models import Task
from apps.tasks.serializers import TaskSerializer
from rest_framework.generics import get_object_or_404


# Это первый подход

# class TaskAPIView(APIView):
#     permission_classes = [IsAuthenticated, ]

#     def get(self, request):
#         tasks = Task.objects.all()
#         serializer = TaskSerializer(tasks, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = TaskSerializer(data=request.data)

#         if serializer.is_valid():
#             owner = request.user
#             task = Task.objects.create(
#                 owner=owner,
#                 text=serializer.validated_data.get('text'),
#                 estimated_finish_time=serializer.validated_data.get('estimated_finish_time')
#             )
#             serializer = TaskSerializer(instance=task)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response({'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# ------------------ второй более простой подход

class TaskListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated,]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, id):
        task = get_object_or_404(Task, id=id)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, id):
        task = get_object_or_404(Task, id=id)
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            update_fields = []
            for field, value in serializer.validated_data.items():
                setattr(task, field, value)
                update_fields.append(field)
            task.save(update_fields=update_fields)

            serializer = TaskSerializer(instance=task)
            return Response(serializer.data)
        return Response({'detail': serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        task = get_object_or_404(Task, id=id)
        task.delete()
        return Response({'detail': f'deleted object #{id}'}, 
                        status=status.HTTP_204_NO_CONTENT)


class SetFinishedTaskAPIView(APIView):

    def get(self, request, id):
        task = get_object_or_404(Task, id=id)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def post(self, request, id, format=None):
        task = get_object_or_404(Task, id=id)
        if task.is_finished:
            task.is_finished = False
        else:
            task.is_finished = True
        task.save()
        serializer = TaskSerializer(instance=task)
        return Response(serializer.data)



