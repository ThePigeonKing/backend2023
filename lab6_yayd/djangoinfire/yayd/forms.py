from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Folder, File, Permission

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['name', 'parent']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['parent'].queryset = Folder.objects.filter(owner=user)

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file', 'folder']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None) 
        super(UploadFileForm, self).__init__(*args, **kwargs)
        if self.user:
            self.fields['folder'].queryset = Folder.objects.filter(owner=self.user)
        

class ShareForm(forms.Form):
    username = forms.CharField(label='Username', max_length=150)
    permission_type = forms.ChoiceField(choices=Permission.PERMISSION_CHOICES, label='Permission Type')