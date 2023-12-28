from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(choices=[(i, str(i)) for i in range(6)], widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Review
        fields = ['text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'text': 'Сообщение',
            'rating': 'Оценка',
        }
