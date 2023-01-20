from django import forms
from . models import Contact, Profile
from products.models import Product, Category


class ContactForm(forms.ModelForm):
    first_name = forms.CharField(required = False, widget = forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'First Name',
        }))
    last_name = forms.CharField(required = False, widget = forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Last Name',
        }))
    email = forms.EmailField(required = False, widget = forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email',
        }))
    message = forms.CharField(widget = forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Message',
        }))

    class Meta():
        model = Contact
        fields = ['first_name', 'last_name', 'email', 'message']

class AddProductForm(forms.ModelForm):
    name = forms.CharField(widget = forms.TextInput(attrs={
        'class': 'edit-profile-input',
        'placeholder': 'Product Name',
        }))
    description = forms.CharField(widget = forms.Textarea(attrs={
        'class': 'edit-profile-input',
        'placeholder': 'Product Description',
        }))
    price = forms.DecimalField(widget = forms.NumberInput(attrs={
        'class': 'edit-profile-input',
        'placeholder': 'Product Price',
        }))
    category = forms.ModelChoiceField(queryset = Category.objects.all() ,widget = forms.Select(attrs={
        'class': 'edit-profile-input',
        'placeholder': 'Product Category',
        }))
    class Meta():
        model = Product
        fields = ['name', 'description', 'category', 'seller', 'image', 'price']
        widgets = {
                'seller': forms.TextInput(attrs = {
                    'class': 'edit-profile-input', 
                    'placeholder': 'Product Name', 
                    'value':'', 
                    'id':'elder', 
                    'type': 'hidden',
                    }),
                'image': forms.FileInput(attrs={
                    'class': 'edit-profile-input',
                    'placeholder': 'First Name',
                    }),
            }

class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(required = False, widget = forms.TextInput(attrs={
        'class': 'edit-profile-input',
        'placeholder': 'First Name',
        }))
    last_name = forms.CharField(required = False, widget = forms.TextInput(attrs={
        'class': 'edit-profile-input',
        'placeholder': 'Last Name',
        }))
    email = forms.EmailField(required = False, widget = forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email',
        }))
    description = forms.CharField(required = False, widget = forms.Textarea(attrs={
        'class': 'edit-profile-input edit-profile-desc',
        'placeholder': 'Edit your profile description.',
        }))
    facebook = forms.URLField(required = False, widget = forms.TextInput(attrs={
        'class': 'edit-profile-input',
        'placeholder': 'Facebook URL',
        }))
    instagram = forms.URLField(required = False, widget = forms.TextInput(attrs={
        'class': 'edit-profile-input',
        'placeholder': 'Instagram URL',
        }))
    twitter = forms.URLField(required = False, widget = forms.TextInput(attrs={
        'class': 'edit-profile-input',
        'placeholder': 'Twitter URL',
        }))
    youtube = forms.URLField(required = False, widget = forms.TextInput(attrs={
        'class': 'edit-profile-input',
        'placeholder': 'Youtube URL',
        }))
    image = forms.ImageField(required = False, widget = forms.TextInput(attrs={
        'class': 'edit-profile-input',
        'placeholder': 'Youtube URL',
        }))
    class Meta():
        model = Profile
        fields = ['first_name', 'last_name','description', 'facebook', 'instagram', 'twitter', 'youtube', 'image']

