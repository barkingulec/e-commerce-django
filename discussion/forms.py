from django import forms
from django.contrib.auth.models import User
from . models import Comment, Discuss

class AddPostForm(forms.ModelForm):
    name = forms.CharField(widget = forms.TextInput(attrs={
        'class': 'add-post-title',
        'placeholder': 'Enter post title',
        }))
    description = forms.CharField(widget = forms.Textarea(attrs={
        'class': 'add-post-desc',
        'placeholder': 'Enter your post',
        }))
    # category = forms.ModelChoiceField(queryset = Category.objects.all() ,widget = forms.Select(attrs={
    #     'class': 'edit-profile-input',
    #     'placeholder': 'Product Category',
    #     }))
    class Meta():
        model = Discuss
        fields = ['name', 'description']
        #widgets = {
                # 'author': forms.TextInput(attrs = {
                #     'class': 'edit-profile-input', 
                #     'placeholder': 'Author Name', 
                #     'value':'', 
                #     'id':'elder2', 
                #     'type': 'hidden',
                #     }),
                # 'image': forms.FileInput(attrs={
                #     'class': 'edit-profile-input',
                #     'placeholder': 'First Name',
                #     }),
            #}

class CommentForm(forms.ModelForm):
    body = forms.CharField(widget = forms.Textarea(attrs={'class': 'comment-input', 'placeholder': 'Type comment here...'}), required = True)
    
    class Meta:
        model = Comment
        fields = ['body']
