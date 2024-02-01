from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .api import get_city_choices
from .models import CitySubscription, Comment


class CitySubscriptionForm(forms.ModelForm):
    city_name = forms.ChoiceField(choices=[])

    class Meta:
        model = CitySubscription
        fields = ["city_name"]

    def __init__(self, *args, **kwargs):
        super(CitySubscriptionForm, self).__init__(*args, **kwargs)
        self.fields["city_name"].choices = get_city_choices()


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
