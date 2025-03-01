from django import forms
from .models import Task
from django.contrib.auth.models import User

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

class RegisterForm(forms.ModelForm):
    username = forms.CharField(required=True, max_length=100)
    email = forms.EmailField(required=True)
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput()
    )
    confirm_password = forms.CharField(required=True, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match')