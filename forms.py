from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
  class Meta:
    model = Task
    fields = ['title', 'description', 'status', 'priority', 'due_date', 'category']

  def clean_due_date(self):
    due_date = self.cleaned_data['due_date']
    if due_date and due_date < timezone.now():
      raise forms.ValidationError("Due date cannot be in the past.")
    return due_date
