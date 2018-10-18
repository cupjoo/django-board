from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Post, Comment


class PostForm(forms.ModelForm):
    type = forms.HiddenInput()

    class Meta:
        model = Post
        fields = ('title', 'content', 'type')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': SummernoteWidget(),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '댓글을 입력해주세요.'
            }),
        }
