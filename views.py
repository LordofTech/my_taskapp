from django.shortcuts import get_object_or_404, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Task
from django.db import models
from .utils import save_task_history

# ... your task views

def update_task(request, pk):
  # ... update task logic
  save_task_history(task, task.serialize())  # Call the function here

# ... other views

@login_required
def update_task(request, pk):
  if request.method == 'PUT':
    task = get_object_or_404(Task, pk=pk, assigned_to=request.user)
    data = request.POST.dict()  # Assuming form data is sent via POST (modify if using PUT request body)
    # Validate data (e.g., using a form or custom validation logic)
    task.title = data.get('title', task.title)  # Update fields based on received data
    task.description = data.get('description', task.description)
    # ... update other fields as needed
    task.save()
    save_task_history(task, task.serialize())  # Track history
    return JsonResponse({'task': task.serialize()}, status=200)
  else:
    return JsonResponse({'error': 'Method not allowed'}, status=405)



@login_required
def create_task(request):
  if request.method == 'POST':
    data = request.POST.dict()  # Get form data as a dictionary
    data['assigned_to'] = request.user.id  # Assign task to current user
    task = Task.objects.create(**data)  # Create task with request data
    return JsonResponse({'task': task.serialize()}, status=201)
  else:
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@login_required
def task_list(request, status=None):
  tasks = Task.objects.filter(assigned_to=request.user)
  if status:
    tasks = tasks.filter(status=status)
  return JsonResponse({'tasks': [task.serialize() for task in tasks]})

@login_required  # Add decorators for update and delete if needed
def task_detail(request, pk):
  task = get_object_or_404(Task, pk=pk, assigned_to=request.user)
  if task.assigned_to != request.user:
    return HttpResponseForbidden()  # Deny access if not assigned user
  # ... rest of the view logic
  return JsonResponse({'task': task.serialize()})

# ... add views for update, delete if needed

def TaskSerializer(task):
  return {
      'id': task.id,
      'title': task.title,
      'description': task.description,
      'status': task.status,
      'priority': task.priority,
      'due_date': task.due_date.isoformat() if task.due_date else None,
      # ... add other relevant fields
  }
