from django.db import models

class Task(models.Model):
  title = models.CharField(max_length=255)
  description = models.TextField()
  STATUS_CHOICES = (
      ('In Progress', 'In Progress'),
      ('Completed', 'Completed'),
      ('Overdue', 'Overdue'),
  )
  status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='In Progress')
  PRIORITY_CHOICES = (
      ('Low', 'Low'),
      ('Medium', 'Medium'),
      ('High', 'High'),
  )
  priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES, default='Medium')
  due_date = models.DateTimeField(blank=True, null=True)
  category = models.CharField(max_length=50, blank=True)
  assigned_to = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True)

  def __str__(self):
    return self.title

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Task

class TaskListView(APIView):
  def get(self, request, format=None):
    status = request.GET.get('status')  # Get status parameter from URL
    tasks = Task.objects.filter(status=status)  # Filter tasks by status
    serializer = TaskSerializer(tasks, many=True)  # Serialize data for JSON response
    return Response(serializer.data)

from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
  class Meta:
    model = Task
    fields = '__all__'  # Include all fields from the Task model

from django.urls import path
from .views import TaskListView  # Import your views

urlpatterns = [
  path('api/tasks/', TaskListView.as_view()),  # Map URL to the TaskListView
]

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer

@api_view(['POST'])
def create_task(request):
  serializer = TaskSerializer(data=request.data)  # Get data from request body
  if serializer.is_valid():
    serializer.save()  # Save the new task to the database
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer

class TaskDetailView(APIView):
  def get(self, request, pk, format=None):
    try:
      task = Task.objects.get(pk=pk)  # Get task by primary key (pk)
      serializer = TaskSerializer(task)  # Serialize task data
      return Response(serializer.data)
    except Task.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)


from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer

class TaskUpdateView(APIView):
  def put(self, request, pk, format=None):
    try:
      task = Task.objects.get(pk=pk)
      serializer = TaskSerializer(task, data=request.data)  # Update task data
      if serializer.is_valid():
        serializer.save()  # Save updated data to the database
        return Response(serializer.data)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Task.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)


from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Task

class TaskDeleteView(APIView):
  def delete(self, request, pk, format=None):
    try:
      task = Task.objects.get(pk=pk)
      task.delete()  # Delete the task from the database
      return Response(status=status.HTTP_204_NO_CONTENT)
    except Task.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)


from django.test import TestCase
from .models import Task

class TaskModelTest(TestCase):
  def test_create_task(self):
    task = Task.objects.create(title="Test Task", description="This is a test task")
    self.assertEqual(task.title, "Test Task")
    self.assertEqual(task.description, "This is a test task")
