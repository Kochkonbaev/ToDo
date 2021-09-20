from apps.tasks.models import Task
from rest_framework import fields, serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username',]


# class TaskSerializer(serializers.Serializer):

#     owner = UserSerializer(read_only=True)
#     text = serializers.CharField()
#     estimated_finish_time = serializers.DateTimeField(format='%d:%m:%Y %H:%M',
#                                             input_formats=['%d:%m:%Y %H:%M',])
#     is_finished = serializers.BooleanField(read_only=True)
    

class TaskSerializer(serializers.ModelSerializer):

    estimated_finish_time = serializers.DateTimeField()
    owner = UserSerializer(read_only=True)
    
    class Meta:
        model = Task
        fields = ['id', 'owner', 'text', 'estimated_finish_time', 'is_finished',]
        read_only_fields = ['is_finished', ]