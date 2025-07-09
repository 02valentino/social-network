from django import forms
from .models import Post
from .models import Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'visibility']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': "What's on your mind?", 'class': 'form-control'}),
            'visibility': forms.Select(attrs={'class': 'form-control'})
        }
        labels = {
            'content': '',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].label = 'Share your thoughts'
        self.fields['visibility'].label = 'Who can see this?'

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Write a comment...',
                'class': 'form-control'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].label = ''