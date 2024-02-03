from django import forms
from .models import Observation

class ObservationForm(forms.ModelForm):
    class Meta:
        model = Observation
        exclude = ['user', 'location']
        widgets = {
            'date_of_review': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
