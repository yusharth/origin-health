from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post,Label


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["author", "label", "image"]

class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['name']

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'label']