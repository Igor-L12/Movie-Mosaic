from django import forms

from .models import Comment, Post

from ckeditor.widgets import CKEditorWidget

class PostForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorWidget(config_name='default'), label='Текст')
    
    class Meta:
        model = Post
        fields = ('title', 'text', 'image')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Добавьте заголовок'},),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)