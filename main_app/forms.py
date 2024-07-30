from django import forms
from .models import Behavior

class BehaviorForm(forms.ModelForm):
    class Meta:
        model = Behavior
        fields = ['date', 'behavior']
        widgets = {
            'date': forms.DateInput(
            format=('%Y-%m-%d'),
            attrs={
                'placeholder': 'Select a date',
                'type': 'date'
            }
          ),
        }
