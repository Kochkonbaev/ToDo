from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.tasks.models import Task
from apps.tasks.serializers import TaskSerializer


class TaskAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)

        if serializer.is_valid():
            owner = request.user
            task = Task.objects.create(
                owner=owner,
                text=serializer.validated_data.get('text'),
                estimated_finish_time=serializer.validated_data.get('estimated_finish_time')
            )
            serializer = TaskSerializer(instance=task)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
