from django.urls import path
from rest_framework.generics import CreateAPIView
from .views import *


urlpatterns = [
    # path('', TaskAPIView.as_view()),
    path('', TaskListView.as_view()),
    path('create/', TaskCreateView.as_view()),
    path('<int:id>/', TaskDetailAPIView.as_view()),
    path('<int:id>/finished/', SetFinishedTaskAPIView.as_view()),

]