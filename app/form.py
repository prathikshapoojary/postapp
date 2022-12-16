from django import forms
from .models import Post


class UploadFileForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ["title","description","type_of_media"]