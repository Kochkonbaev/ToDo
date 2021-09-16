from django.urls import path
from .views import *


urlpatterns = [
    path('', TaskAPIView.as_view()),
    # path('<int:id>/', TaskDetailAPIView.as_view()),
    # path('<int:id>/finished/', SetFinishedTask.as_view()),
]