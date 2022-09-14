from django import forms

from .models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('group', 'text', 'image')
        labels = {
            'text': 'Текст поста',
            'group': 'Группа',
        }
