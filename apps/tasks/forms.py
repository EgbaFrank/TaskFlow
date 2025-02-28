from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    title = forms.CharField(required=True, max_length=100)
    description = forms.CharField(widget=forms.Textarea, required=False)
    completed = forms.BooleanField(required=False)
    due_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'completed', 'due_date']