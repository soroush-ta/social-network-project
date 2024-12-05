from django import forms
from . models import Post, Comment

class PostCreateEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body']


class CommentCreateReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body', 'reply']
    def __init__(self, *args, **kwargs):
        super(CommentCreateReplyForm, self).__init__(*args, **kwargs)
        self.fields['reply'].widget = forms.HiddenInput()  

        