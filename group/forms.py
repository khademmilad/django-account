from django import forms
from .models import Group

class CreateGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = [
            'name',
            'description'
        ]
