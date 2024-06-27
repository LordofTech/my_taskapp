from django.db import models
from django.contrib.auth.models import User


from .utils import save_task_history

# ... your task views

def update_task(request, pk):
  # ... update task logic
  save_task_history(task, task.serialize())  # Call the function here

# ... other views


class TaskHistory(models.Model):
  task = models.ForeignKey(Task, on_delete=models.CASCADE)
  data = models.JSONField()  # Store task data at the time of change
  created_at = models.DateTimeField(auto_now_add=True)

def save_task_history(task, data):
  TaskHistory.objects.create(task=task, data=data)

# In your view logic, call save_task_history before updating the task



class Task(models.Model):
    STATUS_CHOICES = (
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('OVERDUE', 'Overdue'),
    )
    PRIORITY_CHOICES = (
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES)
    due_date = models.DateTimeField(blank=True, null=True)
    category = models.CharField(max_length=50, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    
    

    def __str__(self):
        return self.title
