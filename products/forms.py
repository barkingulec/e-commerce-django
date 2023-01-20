from django import forms
from django.contrib.auth.models import User
from . models import Comment

class CommentForm(forms.ModelForm):
    body = forms.CharField(widget = forms.Textarea(attrs={'class': 'comment-input', 'placeholder': 'Type comment here...'}), required = True)
    
    class Meta:
        model = Comment
        fields = ['body']