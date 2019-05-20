from django import forms
from pagedown.widgets import PagedownWidget
from .models import Post


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget())
    publish = forms.DateField(widget=forms.SelectDateWidget)

    draft = forms.BooleanField(required=False, initial=True)


    class Meta:
        model = Post
        fields = ('category', 'title', 'content', 'image', 'draft', 'publish', 'worksheet_file')
