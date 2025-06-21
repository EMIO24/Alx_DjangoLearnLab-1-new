from django import forms
from .models import ExampleModel  # Import your model

class ExampleForm(forms.ModelForm):
    class Meta:
        model = ExampleModel
        fields = ['name', 'email']  # Include the fields you need

